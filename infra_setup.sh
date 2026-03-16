#!/bin/bash

docker-compose up -d
echo "Waiting for Kafka to be ready..."
# Give it 15-20 seconds to initialize fully
sleep 15

docker exec -it $(docker ps | grep 'bitnami/kafka' | awk '{print $1}') kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 100 \
  --replication-factor 1
  
echo "Setup complete!"