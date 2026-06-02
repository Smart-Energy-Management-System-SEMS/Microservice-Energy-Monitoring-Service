from monitoring.domain.model.repositories.energy_reading_repository import EnergyReadingRepository
from monitoring.domain.model.services.energy_pricing_provider import EnergyPricingProvider
from monitoring.domain.model.valueobjects.energy_price import EnergyPrice


class EnergySimulationQueryService:
    """Read-side service for simulated consumption endpoints."""

    def __init__(
        self,
        reading_repo: EnergyReadingRepository,
        pricing_provider: EnergyPricingProvider,
    ):
        self._reading_repo = reading_repo
        self._pricing_provider = pricing_provider

    async def get_current_price(self) -> EnergyPrice:
        return await self._pricing_provider.get_current_price()

    async def get_current_consumption(self, device_id: str):
        reading = await self._reading_repo.find_latest_by_device(device_id)
        if not reading:
            return None
        price = await self._pricing_provider.get_current_price()
        return reading, price, round(reading.energy_kwh * price.price_per_kwh, 2)

    async def get_consumption_history(self, device_id: str, limit: int = 50, skip: int = 0):
        readings = await self._reading_repo.find_history_by_device(device_id, limit=limit, skip=skip)
        price = await self._pricing_provider.get_current_price()
        return [
            (reading, round(reading.energy_kwh * price.price_per_kwh, 2), price)
            for reading in readings
        ]
