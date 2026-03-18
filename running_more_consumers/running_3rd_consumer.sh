#!/bin/bash

cd producer_consumer_app

# docker build -f consumer/Dockerfile -t my-kafka-consumer:1.0 .


docker run -d --rm \
  --name my_consumer_3 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8003:8001 \
  my-kafka-consumer:1.0