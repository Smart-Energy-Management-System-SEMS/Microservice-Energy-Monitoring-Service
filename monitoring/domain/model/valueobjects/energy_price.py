from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EnergyPrice:
    """Current electricity price from an external provider."""

    provider: str
    price_per_kwh: float
    currency: str
    timestamp: datetime
