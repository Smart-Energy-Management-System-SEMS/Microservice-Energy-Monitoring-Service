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

    @staticmethod
    def _build_event_envelope(
        event_type: str,
        event_id: str,
        occurred_at: str,
        data: dict,
    ) -> dict:
        return {
            "eventId": event_id,
            "eventType": event_type,
            "event_id": event_id,
            "event_type": event_type,
            "occurredAt": occurred_at,
            "occurred_at": occurred_at,
            "data": data,
            **data,
        }

    def publish_reading_processed(self, reading: EnergyReading) -> None:
        """Publish an event when an energy reading has been processed and stored."""
        occurred_at = datetime.utcnow().isoformat()
        event = self._build_event_envelope(
            event_type="energy.reading.processed",
            event_id=str(reading.id),
            occurred_at=occurred_at,
            data={
                "reading_id": reading.id,
                "user_id": reading.user_id,
                "meter_id": reading.meter_id,
                "device_id": reading.device_id,
                "power_watts": reading.power_watts,
                "energy_kwh": reading.energy_kwh,
                "timestamp": reading.timestamp.isoformat() if reading.timestamp else None,
            },
        )
        if KafkaProducer.publish(settings.kafka_topic_energy_events, event):
            logger.info(
                "Published energy.reading.processed to %s for reading_id=%s",
                settings.kafka_topic_energy_events,
                reading.id,
            )

    def publish_energy_reading_created(
        self,
        event_id: str,
        reading: EnergyReading,
        estimated_cost: float,
        currency: str,
    ) -> None:
        occurred_at = datetime.utcnow().isoformat()
        consumption_data = {
            "user_id": reading.user_id,
            "device_id": reading.device_id,
            "reading_id": reading.id,
            "meter_id": reading.meter_id,
            "power_watts": reading.power_watts,
            "energy_kwh": reading.energy_kwh,
            "estimated_cost": estimated_cost,
            "currency": currency,
            "timestamp": reading.timestamp.isoformat() if reading.timestamp else None,
        }
        consumption_event = self._build_event_envelope(
            event_type="energy.consumption.recorded",
            event_id=event_id,
            occurred_at=occurred_at,
            data=consumption_data,
        )
        if KafkaProducer.publish(settings.kafka_topic_energy_events, consumption_event):
            logger.info(
                "Published energy.consumption.recorded to %s for reading_id=%s",
                settings.kafka_topic_energy_events,
                reading.id,
            )

        reading_created_event = self._build_event_envelope(
            event_type="energy.reading.created",
            event_id=event_id,
            occurred_at=occurred_at,
            data=consumption_data,
        )
        if KafkaProducer.publish(settings.kafka_topic_energy_events, reading_created_event):
            logger.info(
                "Published energy.reading.created to %s for reading_id=%s",
                settings.kafka_topic_energy_events,
                reading.id,
            )

    def publish_alert_created(self, alert: ConsumptionAlert) -> None:
        """Publish an event when a consumption alert has been created."""
        occurred_at = datetime.utcnow().isoformat()
        event = self._build_event_envelope(
            event_type="alert.created",
            event_id=str(alert.id),
            occurred_at=occurred_at,
            data={
                "alert_id": alert.id,
                "user_id": alert.user_id,
                "device_id": alert.device_id,
                "meter_id": alert.meter_id,
                "alert_type": alert.alert_type.value,
                "severity": alert.severity.value,
                "message": alert.message,
                "actual_value": alert.actual_value,
                "threshold_value": alert.threshold_value,
            },
        )
        if KafkaProducer.publish(settings.kafka_topic_alerts_events, event):
            logger.info(
                "Published alert.created to %s for alert_id=%s",
                settings.kafka_topic_alerts_events,
                alert.id,
            )
