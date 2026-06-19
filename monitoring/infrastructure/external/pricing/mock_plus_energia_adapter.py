from datetime import datetime, timezone
import random

from monitoring.domain.model.services.energy_pricing_provider import EnergyPricingProvider
from monitoring.domain.model.valueobjects.energy_price import EnergyPrice


class MockPlusEnergiaAdapter(EnergyPricingProvider):
    """Internal mock for the fictitious Plus Energia provider."""

    async def get_current_price(self) -> EnergyPrice:
        now = datetime.now(timezone.utc)
        rng = random.Random(now.strftime("%Y%m%d"))
        price_per_kwh = round(rng.uniform(0.68, 0.92), 2)
        return EnergyPrice(
            provider="Plus Energia",
            price_per_kwh=price_per_kwh,
            currency="PEN",
            timestamp=now,
        )
