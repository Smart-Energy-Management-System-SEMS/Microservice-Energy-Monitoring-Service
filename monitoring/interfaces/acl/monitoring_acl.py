"""
Anti-Corruption Layer (ACL) for the monitoring bounded context.

Translates external event payloads (from IoT Gateway or other microservices)
into internal domain commands, preventing external models from polluting
the domain layer.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from monitoring.domain.model.commands.create_energy_reading_command import CreateEnergyReadingCommand
from monitoring.domain.model.commands.create_consumption_alert_command import CreateConsumptionAlertCommand
from monitoring.domain.model.entities.consumption_alert import AlertType, AlertSeverity
from monitoring.application.services.device_simulation_scheduler import SimulatedDeviceRegistration

logger = logging.getLogger(__name__)


class MonitoringACL:
    """Translates external event data into internal domain commands."""

    @staticmethod
    def to_energy_reading_command(data: Dict[str, Any]) -> Optional[CreateEnergyReadingCommand]:
        """
        Convert an inbound IoT telemetry payload into a CreateEnergyReadingCommand.
        Returns None if required fields are missing.
        """
        try:
            timestamp_raw = data.get("timestamp")
            timestamp = (
                datetime.fromisoformat(timestamp_raw)
                if isinstance(timestamp_raw, str)
                else datetime.utcnow()
            )
            return CreateEnergyReadingCommand(
                user_id=data["user_id"],
                meter_id=data["meter_id"],
                device_id=data.get("device_id", "unknown"),
                power_watts=float(data["power_watts"]),
                voltage=float(data.get("voltage", 220.0)),
                current=float(data.get("current", 0.0)),
                frequency=float(data.get("frequency", 60.0)),
                energy_kwh=float(data.get("energy_kwh", 0.0)),
                timestamp=timestamp,
                reading_type=data.get("reading_type", "real_time"),
                phase=data.get("phase", "single"),
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"ACL translation error (EnergyReading): {e} | data={data}")
            return None

    @staticmethod
    def to_anomaly_alert_command(data: Dict[str, Any]) -> Optional[CreateConsumptionAlertCommand]:
        """
        Convert an inbound anomaly detection event (from Analytics Service)
        into a CreateConsumptionAlertCommand.
        """
        try:
            return CreateConsumptionAlertCommand(
                user_id=data["user_id"],
                device_id=data.get("device_id", "unknown"),
                meter_id=data.get("meter_id", "unknown"),
                alert_type=AlertType.ANOMALY_DETECTED,
                severity=AlertSeverity.HIGH,
                threshold_value=0.0,
                actual_value=float(data.get("score", 0.0)),
                message=data.get("description", "Anomaly detected by analytics engine."),
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"ACL translation error (AnomalyAlert): {e} | data={data}")
            return None

    @staticmethod
    def to_device_registration(data: Dict[str, Any]) -> Optional[SimulatedDeviceRegistration]:
        """
        Convert a device.registered envelope from Device Management into
        the internal representation used by the simulation scheduler.
        """
        try:
            payload = data.get("payload") or {}
            return SimulatedDeviceRegistration(
                user_id=data["userId"],
                device_id=data["deviceId"],
                device_type=payload.get("deviceType", "unknown"),
                status=payload.get("status", data.get("status", "UNKNOWN")),
            )
        except (KeyError, TypeError) as e:
            logger.error(f"ACL translation error (DeviceRegistration): {e} | data={data}")
            return None
