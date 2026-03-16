#!/bin/bash

docker-compose up -d

docker exec -it $(docker ps | grep 'bitnami/kafka' | awk '{print $1}') kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 100 \
  --replication-factor 1

docker load -i my-kafka-producer.tar

docker load -i my-kafka-consumer.tar

docker run -d --rm \
  --name my_producer \
  --network for_candidate_kafka-net \
  -e EXEC_ENV=prod \
  -p 8000:8000 \
  my-kafka-producer:1.0


  docker run -d --rm \
  --name my_consumer \
  --network for_candidate_kafka-net \
  -e EXEC_ENV=prod \
  -p 8001:8001 \
  my-kafka-consumer:1.0