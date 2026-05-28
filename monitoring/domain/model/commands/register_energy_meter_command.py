from dataclasses import dataclass


@dataclass
class RegisterEnergyMeterCommand:
    """Command to register a new smart energy meter for a user."""
    user_id: str
    meter_serial: str
    model: str
    brand: str
    location: str
    firmware_version: str = "1.0.0"
    max_power_watts: float = 10000.0
