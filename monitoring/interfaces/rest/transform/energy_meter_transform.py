from monitoring.domain.model.entities.energy_meter import EnergyMeter
from monitoring.interfaces.rest.resources.energy_meter_resource import EnergyMeterResponse


class EnergyMeterTransform:
    @staticmethod
    def to_response(meter: EnergyMeter) -> EnergyMeterResponse:
        return EnergyMeterResponse(
            id=meter.id,
            user_id=meter.user_id,
            meter_serial=meter.meter_serial,
            model=meter.model,
            brand=meter.brand,
            location=meter.location,
            status=meter.status,
            firmware_version=meter.firmware_version,
            max_power_watts=meter.max_power_watts,
            registered_at=meter.registered_at,
            last_seen_at=meter.last_seen_at,
            updated_at=meter.updated_at,
        )
