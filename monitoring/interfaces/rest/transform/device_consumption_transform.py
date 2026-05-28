from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from monitoring.interfaces.rest.resources.device_consumption_resource import DeviceConsumptionResponse


class DeviceConsumptionTransform:
    @staticmethod
    def to_response(consumption: DeviceConsumption) -> DeviceConsumptionResponse:
        return DeviceConsumptionResponse(
            id=consumption.id,
            user_id=consumption.user_id,
            device_id=consumption.device_id,
            device_name=consumption.device_name,
            meter_id=consumption.meter_id,
            total_kwh=consumption.total_kwh,
            cost_estimate_soles=consumption.cost_estimate_soles,
            period_start=consumption.period_start,
            period_end=consumption.period_end,
            peak_power_watts=consumption.peak_power_watts,
            average_power_watts=consumption.average_power_watts,
            reading_count=consumption.reading_count,
            created_at=consumption.created_at,
            updated_at=consumption.updated_at,
        )
