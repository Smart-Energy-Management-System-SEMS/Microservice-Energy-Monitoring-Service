from abc import ABC, abstractmethod

from monitoring.domain.model.valueobjects.simulated_energy_telemetry import SimulatedEnergyTelemetry


class EosIotProvider(ABC):
    """Port for obtaining telemetry from EOS IoT."""

    @abstractmethod
    async def generate_reading(self, device_id: str, device_type: str = "unknown") -> SimulatedEnergyTelemetry:
        pass
