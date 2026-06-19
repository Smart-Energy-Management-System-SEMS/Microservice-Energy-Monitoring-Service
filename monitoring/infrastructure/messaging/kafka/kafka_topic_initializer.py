import logging

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError

from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class KafkaTopicInitializer:
    """Ensures required Kafka topics exist before producers and consumers use them."""

    @classmethod
    def ensure_topics_exist(cls) -> None:
        if not settings.kafka_enable_topic_init:
            logger.info("Kafka topic initialization disabled by configuration.")
            return

        if settings.is_event_hubs_kafka():
            logger.info("Skipping Kafka topic initialization for Azure Event Hubs.")
            return

        topics = settings.get_kafka_topics()
        if not topics:
            logger.warning("No Kafka topics configured for initialization.")
            return

        logger.info(
            "Ensuring Kafka topics exist. bootstrap_servers=%s topics=%s",
            settings.get_kafka_bootstrap_servers(),
            topics,
        )

        admin = None
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=settings.get_kafka_bootstrap_servers(),
                client_id=f"{settings.service_name}-topic-init",
            )
            existing_topics = set(admin.list_topics())
            missing_topics = [topic for topic in topics if topic not in existing_topics]

            if not missing_topics:
                logger.info("Kafka topics already available.")
                return

            admin.create_topics(
                new_topics=[NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in missing_topics],
                validate_only=False,
            )
            logger.info("Kafka topics created automatically: %s", missing_topics)
        except TopicAlreadyExistsError:
            logger.info("Kafka topics were created concurrently by another client.")
        except KafkaError as exc:
            logger.warning("Kafka topic auto-creation failed: %s", exc, exc_info=True)
        except Exception as exc:
            logger.warning("Unexpected error during Kafka topic initialization: %s", exc, exc_info=True)
        finally:
            if admin is not None:
                admin.close()
