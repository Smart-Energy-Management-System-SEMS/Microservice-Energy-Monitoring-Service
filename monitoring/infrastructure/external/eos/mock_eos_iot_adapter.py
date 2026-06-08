from datetime import datetime, timezone
import random
import math

from monitoring.domain.model.services.eos_iot_provider import EosIotProvider
from monitoring.domain.model.valueobjects.simulated_energy_telemetry import SimulatedEnergyTelemetry


class MockEosIotAdapter(EosIotProvider):
    """Internal mock for the fictitious EOS IoT system."""

    DEVICE_PROFILES = {
        "mobile": {"base_power": 8.0, "swing": 10.0, "phase": "single", "voltage": (5.0, 12.0)},
        "phone": {"base_power": 8.0, "swing": 10.0, "phase": "single", "voltage": (5.0, 12.0)},
        "tablet": {"base_power": 12.0, "swing": 12.0, "phase": "single", "voltage": (5.0, 15.0)},
        "laptop": {"base_power": 45.0, "swing": 35.0, "phase": "single", "voltage": (19.0, 20.0)},
        "tv": {"base_power": 90.0, "swing": 50.0, "phase": "single", "voltage": (215.0, 235.0)},
        "refrigerator": {"base_power": 150.0, "swing": 90.0, "phase": "single", "voltage": (215.0, 235.0)},
        "thermostat": {"base_power": 18.0, "swing": 20.0, "phase": "single", "voltage": (18.0, 24.0)},
        "airconditioner": {"base_power": 1100.0, "swing": 600.0, "phase": "single", "voltage": (215.0, 235.0)},
        "washer": {"base_power": 500.0, "swing": 450.0, "phase": "single", "voltage": (215.0, 235.0)},
        "washingmachine": {"base_power": 500.0, "swing": 450.0, "phase": "single", "voltage": (215.0, 235.0)},
        "dryer": {"base_power": 1800.0, "swing": 500.0, "phase": "three", "voltage": (380.0, 405.0)},
        "microwave": {"base_power": 900.0, "swing": 250.0, "phase": "single", "voltage": (215.0, 235.0)},
        "heater": {"base_power": 1400.0, "swing": 500.0, "phase": "single", "voltage": (215.0, 235.0)},
        "sensor": {"base_power": 3.0, "swing": 2.0, "phase": "single", "voltage": (3.0, 5.0)},
        "unknown": {"base_power": 120.0, "swing": 80.0, "phase": "single", "voltage": (215.0, 235.0)},
    }

    async def generate_reading(self, device_id: str, device_type: str = "unknown") -> SimulatedEnergyTelemetry:
        now = datetime.now(timezone.utc)
        seed = f"{device_id}:{device_type}:{now.strftime('%Y%m%d%H')}"
        rng = random.Random(seed)
        profile = self._resolve_profile(device_type)

        phase = profile["phase"]
        voltage_range = profile["voltage"]
        voltage = round(rng.uniform(*voltage_range), 2)
        power_watts = round(self._build_power_watts(profile, now.hour, rng), 2)
        current = round(power_watts / voltage, 3)
        frequency = round(rng.uniform(59.7, 60.3), 2)
        reading_type = rng.choices(
            population=["real_time", "scheduled", "on_demand"],
            weights=[0.2, 0.75, 0.05],
            k=1,
        )[0]
        utilization = rng.uniform(0.75, 1.05)
        energy_kwh = round(max(0.001, power_watts / 1000 * utilization), 3)

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

    def _resolve_profile(self, device_type: str) -> dict:
        normalized = "".join(ch for ch in device_type.lower() if ch.isalnum()) if device_type else "unknown"
        return self.DEVICE_PROFILES.get(normalized, self.DEVICE_PROFILES["unknown"])

    def _build_power_watts(self, profile: dict, hour: int, rng: random.Random) -> float:
        base_power = profile["base_power"]
        swing = profile["swing"]

        # Two daily peaks create a home-like pattern without unrealistic spikes.
        morning_peak = max(0.0, math.sin(((hour - 6) / 24) * 2 * math.pi))
        evening_peak = max(0.0, math.sin(((hour - 18) / 24) * 2 * math.pi))
        daily_factor = 0.82 + (morning_peak * 0.12) + (evening_peak * 0.18)
        random_factor = rng.uniform(0.92, 1.08)
        burst_factor = rng.uniform(0.0, 1.0)

        power = (base_power * daily_factor * random_factor) + (swing * burst_factor)
        lower_bound = max(1.0, base_power * 0.55)
        upper_bound = base_power + swing
        return min(max(power, lower_bound), upper_bound)
