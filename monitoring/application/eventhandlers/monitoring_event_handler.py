import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from monitoring.infrastructure.messaging.kafka.kafka_consumer import KafkaConsumer
from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class MonitoringEventHandler:
    """
    Application event handler that registers Kafka consumer callbacks
    for inbound events from other bounded contexts (e.g., IoT gateway,
    Analytics Service).
    """

    def __init__(self, kafka_consumer: KafkaConsumer):
        self._kafka_consumer = kafka_consumer

    def register_handlers(self) -> None:
        """Register all topic handlers with the Kafka consumer."""
        self._kafka_consumer.register_handler(
            settings.kafka_topic_reading_ingest,
            self._handle_reading_ingest,
        )
        self._kafka_consumer.register_handler(
            settings.kafka_topic_anomaly_detected,
            self._handle_anomaly_detected,
        )
        logger.info("MonitoringEventHandler: all Kafka handlers registered.")

    def _handle_reading_ingest(self, data: Dict[str, Any]) -> None:
        """
        Handle raw telemetry event received from IoT Gateway via Kafka.
        In a real system this would invoke the EnergyReadingCommandService asynchronously.
        """
        if not data:
            return
        logger.info(
            f"[Kafka] EnergyReading ingest received: "
            f"meter_id={data.get('meter_id')}, "
            f"power_watts={data.get('power_watts')}"
        )
        # TODO: dispatch to EnergyReadingCommandService via asyncio event loop
        # asyncio.run_coroutine_threadsafe(command_service.handle_create(cmd), loop)

    def _handle_anomaly_detected(self, data: Dict[str, Any]) -> None:
        """
        Handle anomaly detection event received from the Analytics Service via Kafka.
        Creates a ConsumptionAlert of type ANOMALY_DETECTED.
        """
        if not data:
            return
        logger.warning(
            f"[Kafka] Anomaly detected from Analytics: "
            f"user_id={data.get('user_id')}, "
            f"device_id={data.get('device_id')}, "
            f"score={data.get('score')}"
        )
        # TODO: dispatch to ConsumptionAlertCommandService via asyncio event loop
