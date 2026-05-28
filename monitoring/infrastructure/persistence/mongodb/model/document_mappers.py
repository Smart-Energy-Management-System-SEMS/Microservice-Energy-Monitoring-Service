from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert, AlertType, AlertSeverity
from monitoring.domain.model.entities.energy_meter import EnergyMeter, MeterStatus


def _str_id(doc: Dict[str, Any]) -> str:
    return str(doc["_id"])


class EnergyReadingDocumentMapper:
    @staticmethod
    def to_document(reading: EnergyReading) -> Dict[str, Any]:
        doc = {
            "user_id": reading.user_id,
            "meter_id": reading.meter_id,
            "device_id": reading.device_id,
            "power_watts": reading.power_watts,
            "voltage": reading.voltage,
            "current": reading.current,
            "frequency": reading.frequency,
            "energy_kwh": reading.energy_kwh,
            "timestamp": reading.timestamp,
            "reading_type": reading.reading_type,
            "phase": reading.phase,
            "created_at": reading.created_at,
        }
        if reading.id:
            doc["_id"] = ObjectId(reading.id)
        return doc

    @staticmethod
    def to_entity(doc: Dict[str, Any]) -> EnergyReading:
        return EnergyReading(
            id=_str_id(doc),
            user_id=doc["user_id"],
            meter_id=doc["meter_id"],
            device_id=doc["device_id"],
            power_watts=doc["power_watts"],
            voltage=doc["voltage"],
            current=doc["current"],
            frequency=doc["frequency"],
            energy_kwh=doc["energy_kwh"],
            timestamp=doc["timestamp"],
            reading_type=doc.get("reading_type", "real_time"),
            phase=doc.get("phase", "single"),
            created_at=doc.get("created_at", datetime.utcnow()),
        )


class DeviceConsumptionDocumentMapper:
    @staticmethod
    def to_document(consumption: DeviceConsumption) -> Dict[str, Any]:
        doc = {
            "user_id": consumption.user_id,
            "device_id": consumption.device_id,
            "device_name": consumption.device_name,
            "meter_id": consumption.meter_id,
            "total_kwh": consumption.total_kwh,
            "cost_estimate_soles": consumption.cost_estimate_soles,
            "period_start": consumption.period_start,
            "period_end": consumption.period_end,
            "peak_power_watts": consumption.peak_power_watts,
            "average_power_watts": consumption.average_power_watts,
            "reading_count": consumption.reading_count,
            "created_at": consumption.created_at,
            "updated_at": consumption.updated_at,
        }
        if consumption.id:
            doc["_id"] = ObjectId(consumption.id)
        return doc

    @staticmethod
    def to_entity(doc: Dict[str, Any]) -> DeviceConsumption:
        return DeviceConsumption(
            id=_str_id(doc),
            user_id=doc["user_id"],
            device_id=doc["device_id"],
            device_name=doc["device_name"],
            meter_id=doc["meter_id"],
            total_kwh=doc["total_kwh"],
            cost_estimate_soles=doc["cost_estimate_soles"],
            period_start=doc["period_start"],
            period_end=doc["period_end"],
            peak_power_watts=doc["peak_power_watts"],
            average_power_watts=doc["average_power_watts"],
            reading_count=doc["reading_count"],
            created_at=doc.get("created_at", datetime.utcnow()),
            updated_at=doc.get("updated_at", datetime.utcnow()),
        )


class ConsumptionAlertDocumentMapper:
    @staticmethod
    def to_document(alert: ConsumptionAlert) -> Dict[str, Any]:
        doc = {
            "user_id": alert.user_id,
            "device_id": alert.device_id,
            "meter_id": alert.meter_id,
            "alert_type": alert.alert_type.value,
            "severity": alert.severity.value,
            "threshold_value": alert.threshold_value,
            "actual_value": alert.actual_value,
            "message": alert.message,
            "is_read": alert.is_read,
            "is_resolved": alert.is_resolved,
            "created_at": alert.created_at,
            "resolved_at": alert.resolved_at,
        }
        if alert.id:
            doc["_id"] = ObjectId(alert.id)
        return doc

    @staticmethod
    def to_entity(doc: Dict[str, Any]) -> ConsumptionAlert:
        return ConsumptionAlert(
            id=_str_id(doc),
            user_id=doc["user_id"],
            device_id=doc["device_id"],
            meter_id=doc["meter_id"],
            alert_type=AlertType(doc["alert_type"]),
            severity=AlertSeverity(doc["severity"]),
            threshold_value=doc["threshold_value"],
            actual_value=doc["actual_value"],
            message=doc["message"],
            is_read=doc.get("is_read", False),
            is_resolved=doc.get("is_resolved", False),
            created_at=doc.get("created_at", datetime.utcnow()),
            resolved_at=doc.get("resolved_at"),
        )


class EnergyMeterDocumentMapper:
    @staticmethod
    def to_document(meter: EnergyMeter) -> Dict[str, Any]:
        doc = {
            "user_id": meter.user_id,
            "meter_serial": meter.meter_serial,
            "model": meter.model,
            "brand": meter.brand,
            "location": meter.location,
            "status": meter.status.value,
            "firmware_version": meter.firmware_version,
            "max_power_watts": meter.max_power_watts,
            "registered_at": meter.registered_at,
            "last_seen_at": meter.last_seen_at,
            "updated_at": meter.updated_at,
        }
        if meter.id:
            doc["_id"] = ObjectId(meter.id)
        return doc

    @staticmethod
    def to_entity(doc: Dict[str, Any]) -> EnergyMeter:
        return EnergyMeter(
            id=_str_id(doc),
            user_id=doc["user_id"],
            meter_serial=doc["meter_serial"],
            model=doc["model"],
            brand=doc["brand"],
            location=doc["location"],
            status=MeterStatus(doc.get("status", "active")),
            firmware_version=doc.get("firmware_version", "1.0.0"),
            max_power_watts=doc.get("max_power_watts", 10000.0),
            registered_at=doc.get("registered_at", datetime.utcnow()),
            last_seen_at=doc.get("last_seen_at"),
            updated_at=doc.get("updated_at", datetime.utcnow()),
        )
