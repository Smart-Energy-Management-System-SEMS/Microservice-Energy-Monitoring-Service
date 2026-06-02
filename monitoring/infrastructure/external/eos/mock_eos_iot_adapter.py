from datetime import datetime, timezone
import random

from monitoring.domain.model.services.eos_iot_provider import EosIotProvider
from monitoring.domain.model.valueobjects.simulated_energy_telemetry import SimulatedEnergyTelemetry


class MockEosIotAdapter(EosIotProvider):
    """Internal mock for the fictitious EOS IoT system."""

    async def generate_reading(self, device_id: str) -> SimulatedEnergyTelemetry:
        now = datetime.now(timezone.utc)
        seed = f"{device_id}:{now.strftime('%Y%m%d%H%M')}"
        rng = random.Random(seed)

        phase = "three" if rng.random() >= 0.65 else "single"
        voltage = round(rng.uniform(215.0, 235.0) if phase == "single" else rng.uniform(380.0, 415.0), 2)
        power_watts = round(rng.uniform(250.0, 2400.0), 2)
        current = round(power_watts / voltage, 3)
        frequency = round(rng.uniform(59.7, 60.3), 2)
        reading_type = rng.choices(
            population=["real_time", "scheduled", "on_demand"],
            weights=[0.7, 0.2, 0.1],
            k=1,
        )[0]
        energy_kwh = round(power_watts / 1000 * rng.uniform(0.4, 1.6), 3)

        return SimulatedEnergyTelemetry(
            power_watts=power_watts,
            voltage=voltage,
            current=current,
            frequency=frequency,
            energy_kwh=energy_kwh,
            timestamp=now,
            reading_type=reading_type,
            phase=phase,
        )
