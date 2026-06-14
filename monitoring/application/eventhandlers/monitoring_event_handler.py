import logging
import asyncio
from typing import Dict, Any
from monitoring.infrastructure.messaging.kafka.kafka_consumer import KafkaConsumer
from monitoring.infrastructure.configuration.settings import settings
from monitoring.interfaces.acl.monitoring_acl import MonitoringACL
from monitoring.application.services.device_simulation_scheduler import DeviceSimulationScheduler

logger = logging.getLogger(__name__)


class MonitoringEventHandler:
    """
    Application event handler that registers Kafka consumer callbacks
    for inbound events from other bounded contexts (e.g., IoT gateway,
    Analytics Service).
    """

    def __init__(
        self,
        kafka_consumer: KafkaConsumer,
        event_loop: asyncio.AbstractEventLoop,
        simulation_scheduler: DeviceSimulationScheduler,
    ):
        self._kafka_consumer = kafka_consumer
        self._event_loop = event_loop
        self._simulation_scheduler = simulation_scheduler

    def register_handlers(self) -> None:
        """Register all topic handlers with the Kafka consumer."""
        self._kafka_consumer.register_handler(
            settings.kafka_topic_device_events,
            self._handle_device_registered,
        )
        self._kafka_consumer.register_handler(
            settings.kafka_topic_energy_events,
            self._handle_reading_ingest,
        )
        self._kafka_consumer.register_handler(
            settings.kafka_topic_analytics_events,
            self._handle_anomaly_detected,
        )
        logger.info("MonitoringEventHandler: all Kafka handlers registered.")

    @staticmethod
    def _matches_event(data: Dict[str, Any], expected_event_type: str, fallback_topic: str) -> bool:
        if not isinstance(data, dict):
            return False
        event_type = MonitoringACL.get_event_type(data)
        if event_type:
            return event_type == expected_event_type
        return data.get("_topic") == fallback_topic

    def _handle_device_registered(self, data: Dict[str, Any]) -> None:
        """Start an automatic simulation loop for newly registered active devices."""
        if not self._matches_event(data, "device.registered", settings.kafka_topic_device_events):
            return

        registration = MonitoringACL.to_device_registration(data)
        if registration is None:
            return

        logger.info(
            "[Kafka] Device registered received: device_id=%s user_id=%s status=%s",
            registration.device_id,
            registration.user_id,
            registration.status,
        )
        asyncio.run_coroutine_threadsafe(
            self._simulation_scheduler.activate_device(registration),
            self._event_loop,
        )

    def _handle_reading_ingest(self, data: Dict[str, Any]) -> None:
        """
        Handle raw telemetry event received from IoT Gateway via Kafka.
        In a real system this would invoke the EnergyReadingCommandService asynchronously.
        """
        if not data:
            return
        if not self._matches_event(data, "energy.reading.ingested", settings.kafka_topic_energy_events):
            return
        payload = MonitoringACL.get_event_payload(data)
        logger.info(
            f"[Kafka] EnergyReading ingest received: "
            f"meter_id={payload.get('meter_id')}, "
            f"power_watts={payload.get('power_watts')}"
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
        if not self._matches_event(data, "analytics.anomaly.detected", settings.kafka_topic_analytics_events):
            return
        payload = MonitoringACL.get_event_payload(data)
        logger.warning(
            f"[Kafka] Anomaly detected from Analytics: "
            f"user_id={payload.get('user_id')}, "
            f"device_id={payload.get('device_id')}, "
            f"score={payload.get('score')}"
        )
        # TODO: dispatch to ConsumptionAlertCommandService via asyncio event loop
