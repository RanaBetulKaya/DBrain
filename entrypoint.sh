#!/bin/bash

# Kafka başlatılırken otomatik olarak topic oluşturma
echo "Creating Kafka topic..."
/opt/kafka_2.13-2.8.1/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic DBrainTask

# Kafka broker'ı başlatma
/opt/kafka_2.13-2.8.1/bin/kafka-server-start.sh /opt/kafka_2.13-2.8.1/config/server.properties
