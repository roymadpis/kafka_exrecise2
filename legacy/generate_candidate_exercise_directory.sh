#!/bin/bash

mkdir for_candidate

cp prometheus.yml for_candidate/

cp docker-compose.yml for_candidate/

cp exercise_setup.sh for_candidate/

chmod +x for_candidate/exercise_setup.sh

cp producer_consumer_app/schemas/message.proto for_candidate/

cd producer_consumer_app

docker build -f producer/Dockerfile -t my-kafka-producer:1.0 .

docker build -f consumer/Dockerfile -t my-kafka-consumer:1.0 .

cd ..

docker save -o for_candidate/my-kafka-producer.tar my-kafka-producer:1.0

docker save -o for_candidate/my-kafka-consumer.tar my-kafka-consumer:1.0
