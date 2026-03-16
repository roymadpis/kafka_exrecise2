from prometheus_client import start_http_server, Counter, Histogram
from kafka import KafkaConsumer
from schemas import message_pb2
import yaml
import time
import os
import random

CONSUMER_GROUP = 'my-consumergroup'

execution_env = os.getenv("EXEC_ENV", "local")
with open(f"config/{execution_env}.yml", "r") as f:
    config = yaml.safe_load(f)
    bootstrap_servers = config['Kafka']['bootstrap_servers']
    topic_name = config['Kafka']['topic_name']

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=CONSUMER_GROUP,
    max_poll_records=1
)

messages_consumed = Counter(
    'messages_consumed', 
    'Total messages consumed',
    ['partition', 'consumer_group']
)
### Roy: adding latency histogram to measure time from producing to consuming a message.
# This requires the producer to include a timestamp in the message, and the consumer to calculate the latency based on that timestamp.
latency_histogram = Histogram(
    'message_processing_latency_seconds', 
    'Total time from producing to consuming (End-to-End)',
    #buckets = [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 15, 20, 100, 200],
    buckets = [0.1, 1, 5, 10, 20, 100, 200, 400, 800],
)

# Queue Time: Broker/Send to Now
queue_time_histogram = Histogram(
    'message_queue_time_seconds',
    'Time message spent sitting in Kafka topic (Consumer Lag)',
    buckets=[0.1, 1, 5, 10, 20, 100, 200, 400, 800],
)

start_http_server(8001)
while True:
    random_timeout_ms = random.randint(500, 1500) # Simulate variable processing time
    records = consumer.poll(timeout_ms=random_timeout_ms) #timeout_ms is the max time to block waiting for records. We can set it to a lower value to have more frequent polls, or higher value to reduce CPU usage when there are no messages.
    #records = consumer.poll(timeout_ms=1000) #timeout_ms is the max time to block waiting for records. We can set it to a lower value to have more frequent polls, or higher value to reduce CPU usage when there are no messages.

    for topic_partition, messages in records.items():
        partition_id = topic_partition.partition

        print(f"Consumed: {len(messages)} from partition #{partition_id}")

        for message in messages:
            
            value_bytes = message.value

            try:
                # Extract the 'send_time' from Kafka Headers
                send_time_ms = None
                if message.headers:
                    for key, value in message.headers:
                        if key == 'send_time':
                            send_time_ms = int(value.decode('utf-8'))
                            break
                # Deserialize Protobuf message
                msg = message_pb2.MyMessage()
                msg.ParseFromString(value_bytes)

                # Timestamps for calculation
                current_time_ms = int(round(time.time() * 1000))
                birth_time_ms = msg.timestamp # From Protobuf

                # 3. Calculate and Observe Metrics
                # Total End-to-End
                total_latency_sec = (current_time_ms - birth_time_ms) / 1000.0
                latency_histogram.observe(total_latency_sec)
                
                # Time in Queue (Consumer Lag)
                if send_time_ms:
                    queue_sec = (current_time_ms - send_time_ms) / 1000.0
                    queue_time_histogram.observe(queue_sec)
                    
                    
                    
                # Access fields
                timestamp = msg.timestamp
                contents = msg.contents
                print(f"Received: {timestamp=}, {contents=}, from partition #{partition_id}")

                ### compute latency and observe it in the histogram - for prometheus
                # current_time_in_ms = int(round(time.time() * 1000))
                # latency_in_ms = current_time_in_ms - timestamp
                # latency_histogram.observe(latency_in_ms / 1000.0) #record latency in seconds for Prometheus
                
                messages_consumed.labels(
                    partition=str(partition_id), 
                    consumer_group=CONSUMER_GROUP
                ).inc()

                ### settting random sleep to simulate variable processing time and to make the latency histogram more interesting. In a real application, this would be the actual processing time of the message.
                random_sleep = random.uniform(0, 1.2) # Simulate variable processing time
                time.sleep(random_sleep)
                #time.sleep(1)

            except Exception as e:
                print(f"ERROR: Failed to parse message from partition {partition_id}: {e}")
