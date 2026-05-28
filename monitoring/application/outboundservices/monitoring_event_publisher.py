import json
import logging
from datetime import datetime
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert
from monitoring.infrastructure.messaging.kafka.kafka_producer import KafkaProducer
from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class MonitoringEventPublisher:
    """
    Outbound service responsible for publishing domain events
    from the monitoring bounded context to Kafka topics.
    """

    def publish_reading_processed(self, reading: EnergyReading) -> None:
        """Publish an event when an energy reading has been processed and stored."""
        event = {
            "event_type": "EnergyReadingProcessed",
            "reading_id": reading.id,
            "user_id": reading.user_id,
            "meter_id": reading.meter_id,
            "device_id": reading.device_id,
            "power_watts": reading.power_watts,
            "energy_kwh": reading.energy_kwh,
            "timestamp": reading.timestamp.isoformat() if reading.timestamp else None,
            "occurred_at": datetime.utcnow().isoformat(),
        }
        KafkaProducer.publish(settings.kafka_topic_reading_processed, event)
        logger.info(f"Published EnergyReadingProcessed for reading_id={reading.id}")

    def publish_alert_created(self, alert: ConsumptionAlert) -> None:
        """Publish an event when a consumption alert has been created."""
        event = {
            "event_type": "ConsumptionAlertCreated",
            "alert_id": alert.id,
            "user_id": alert.user_id,
            "device_id": alert.device_id,
            "meter_id": alert.meter_id,
            "alert_type": alert.alert_type.value,
            "severity": alert.severity.value,
            "message": alert.message,
            "actual_value": alert.actual_value,
            "threshold_value": alert.threshold_value,
            "occurred_at": datetime.utcnow().isoformat(),
        }
        KafkaProducer.publish(settings.kafka_topic_alert_created, event)
        logger.info(f"Published ConsumptionAlertCreated for alert_id={alert.id}")
