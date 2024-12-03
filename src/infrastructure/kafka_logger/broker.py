from faststream.kafka import KafkaBroker

from src.config import KafkaConfig


def kafka_broker_factory(kafka_conf: KafkaConfig) -> KafkaBroker:
    broker = KafkaBroker(kafka_conf.uri)
    return broker
