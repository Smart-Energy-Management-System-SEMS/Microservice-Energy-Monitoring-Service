from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.interfaces.rest.resources.energy_reading_resource import EnergyReadingResponse


class EnergyReadingTransform:
    @staticmethod
    def to_response(reading: EnergyReading) -> EnergyReadingResponse:
        return EnergyReadingResponse(
            id=reading.id,
            user_id=reading.user_id,
            meter_id=reading.meter_id,
            device_id=reading.device_id,
            power_watts=reading.power_watts,
            voltage=reading.voltage,
            current=reading.current,
            frequency=reading.frequency,
            energy_kwh=reading.energy_kwh,
            timestamp=reading.timestamp,
            reading_type=reading.reading_type,
            phase=reading.phase,
            created_at=reading.created_at,
        )
