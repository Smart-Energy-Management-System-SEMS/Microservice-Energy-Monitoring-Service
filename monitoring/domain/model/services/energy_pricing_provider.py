from abc import ABC, abstractmethod

from monitoring.domain.model.valueobjects.energy_price import EnergyPrice


class EnergyPricingProvider(ABC):
    """Port for obtaining current electricity pricing."""

    @abstractmethod
    async def get_current_price(self) -> EnergyPrice:
        pass
