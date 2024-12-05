@echo off

docker compose pull
docker compose build

docker compose up -d postgres zookeeper kafka kafka-ui
echo Wait 5 seconds for containers start...
timeout /t 5

docker compose up -d migrations
docker compose up -d app
