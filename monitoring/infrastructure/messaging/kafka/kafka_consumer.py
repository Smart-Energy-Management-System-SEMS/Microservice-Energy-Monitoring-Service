import json
import logging
import threading
from typing import Callable, Dict, Any
from kafka import KafkaConsumer as _KafkaConsumer
from kafka.errors import KafkaError
from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """
    Kafka consumer that listens to configured topics and dispatches
    messages to registered handler callbacks.
    """

    def __init__(self):
        self._consumer: _KafkaConsumer = None
        self._handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self._running = False
        self._thread: threading.Thread = None

    def register_handler(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a handler function for a specific Kafka topic."""
        self._handlers[topic] = handler
        logger.info(f"Handler registered for topic: {topic}")

    def _build_consumer(self) -> _KafkaConsumer:
        topics = list(self._handlers.keys())
        return _KafkaConsumer(
            *topics,
            bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
            group_id=settings.kafka_group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")) if v else None,
            consumer_timeout_ms=1000,
        )

    def _consume_loop(self) -> None:
        logger.info("Kafka consumer loop started.")
        try:
            self._consumer = self._build_consumer()
            while self._running:
                try:
                    records = self._consumer.poll(timeout_ms=500)
                    for tp, messages in records.items():
                        topic = tp.topic
                        handler = self._handlers.get(topic)
                        if handler:
                            for msg in messages:
                                try:
                                    handler(msg.value)
                                except Exception as e:
                                    logger.error(f"Error handling message from {topic}: {e}", exc_info=True)
                except KafkaError as e:
                    logger.error(f"Kafka poll error: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Fatal error in Kafka consumer loop: {e}", exc_info=True)
        finally:
            if self._consumer:
                self._consumer.close()
                logger.info("Kafka consumer closed.")

    def start(self) -> None:
        if not self._handlers:
            logger.warning("No Kafka handlers registered. Consumer not started.")
            return
        self._running = True
        self._thread = threading.Thread(target=self._consume_loop, daemon=True)
        self._thread.start()
        logger.info("Kafka consumer thread started.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Kafka consumer stopped.")
