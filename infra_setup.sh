#!/bin/bash

docker-compose up -d
echo "Waiting for Kafka to be ready..."
# Give it 15-20 seconds to initialize fully
sleep 10

docker exec $(docker ps | grep 'confluentinc/cp-kafka' | awk '{print $1}') kafka-topics --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 15 \
  --replication-factor 1

## docker compose exec kafka kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 100 --replication-factor 1
echo "Setup complete!"