#!/bin/bash

docker-compose pull
docker-compose build

docker-compose up -d postgres zookeeper kafka kafka-ui
echo "Wait 5 seconds for containers start..."
sleep 5

docker-compose up -d migrations app
