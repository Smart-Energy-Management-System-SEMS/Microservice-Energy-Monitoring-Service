from dataclasses import dataclass


@dataclass(frozen=True)
class PowerReading:
    """
    Value Object: Immutable representation of a power measurement.
    Encapsulates the electrical measurements from a smart meter.
    """
    power_watts: float
    voltage: float
    current: float
    frequency: float
    energy_kwh: float

    def __post_init__(self):
        if self.power_watts < 0:
            raise ValueError("Power watts cannot be negative.")
        if self.voltage < 0:
            raise ValueError("Voltage cannot be negative.")
        if self.current < 0:
            raise ValueError("Current cannot be negative.")
        if not (45.0 <= self.frequency <= 65.0):
            raise ValueError("Frequency must be between 45 and 65 Hz.")

    def apparent_power_va(self) -> float:
        return self.voltage * self.current

    def power_factor(self) -> float:
        apparent = self.apparent_power_va()
        if apparent == 0:
            return 1.0
        return min(self.power_watts / apparent, 1.0)
