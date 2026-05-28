import json
import logging
from kafka import KafkaProducer as _KafkaProducer
from kafka.errors import KafkaError
from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class KafkaProducer:
    """
    Kafka producer for publishing domain events to configured topics.
    Uses a singleton pattern within the application lifecycle.
    """

    _instance: "_KafkaProducer" = None

    @classmethod
    def _get_producer(cls) -> _KafkaProducer:
        if cls._instance is None:
            kwargs = {
                "bootstrap_servers": settings.kafka_bootstrap_servers.split(","),
                "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
                "retries": 3,
                "acks": "all",
                "security_protocol": settings.kafka_security_protocol,
            }
            if settings.kafka_sasl_mechanism and settings.kafka_sasl_username and settings.kafka_sasl_password:
                kwargs.update(
                    {
                        "sasl_mechanism": settings.kafka_sasl_mechanism,
                        "sasl_plain_username": settings.kafka_sasl_username,
                        "sasl_plain_password": settings.kafka_sasl_password,
                    }
                )
            cls._instance = _KafkaProducer(
                **kwargs,
            )
        return cls._instance

    @classmethod
    def publish(cls, topic: str, message: dict) -> None:
        """
        Publish a message dict to the given Kafka topic.
        Logs the result and handles errors gracefully.
        """
        try:
            producer = cls._get_producer()
            future = producer.send(topic, value=message)
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Message published to topic '{record_metadata.topic}' "
                f"[partition={record_metadata.partition}, offset={record_metadata.offset}]"
            )
        except KafkaError as e:
            logger.error(f"Failed to publish message to topic '{topic}': {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error publishing to topic '{topic}': {e}", exc_info=True)

    @classmethod
    def close(cls) -> None:
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None
            logger.info("Kafka producer closed.")
