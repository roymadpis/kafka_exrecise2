#!/bin/bash

cd producer_consumer_app

# docker build -f consumer/Dockerfile -t my-kafka-consumer:1.0 .



docker run -d --rm \
  --name my_consumer_4 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8004:8001 \
  my-kafka-consumer:1.0


docker run -d --rm \
  --name my_consumer_5 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8005:8001 \
  my-kafka-consumer:1.0

  docker run -d --rm \
  --name my_consumer_6 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8006:8001 \
  my-kafka-consumer:1.0


  docker run -d --rm \
  --name my_consumer_7 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8007:8001 \
  my-kafka-consumer:1.0


  docker run -d --rm \
  --name my_consumer_8 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8008:8001 \
  my-kafka-consumer:1.0


    docker run -d --rm \
  --name my_consumer_9 \
  --network kafka_exrecise2_kafka-net \
  -e EXEC_ENV=prod \
  -p 8009:8001 \
  my-kafka-consumer:1.0