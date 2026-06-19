from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.valueobjects.energy_price import EnergyPrice
from monitoring.interfaces.rest.resources.energy_simulation_resource import (
    CurrentConsumptionResponse,
    EnergyPricingResponse,
    SimulatedEnergyReadingResponse,
)


class EnergySimulationTransform:
    @staticmethod
    def to_pricing_response(price: EnergyPrice) -> EnergyPricingResponse:
        return EnergyPricingResponse(
            provider=price.provider,
            price_per_kwh=price.price_per_kwh,
            currency=price.currency,
            timestamp=price.timestamp,
        )

    @staticmethod
    def to_reading_response(
        reading: EnergyReading,
        price: EnergyPrice,
        estimated_cost: float,
    ) -> SimulatedEnergyReadingResponse:
        return SimulatedEnergyReadingResponse(
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
            estimated_cost=estimated_cost,
            currency=price.currency,
            provider=price.provider,
        )

    @staticmethod
    def to_current_response(
        reading: EnergyReading,
        price: EnergyPrice,
        estimated_cost: float,
    ) -> CurrentConsumptionResponse:
        return CurrentConsumptionResponse(**EnergySimulationTransform.to_reading_response(reading, price, estimated_cost).model_dump())
