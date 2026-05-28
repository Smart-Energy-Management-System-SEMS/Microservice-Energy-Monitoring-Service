from dataclasses import dataclass


@dataclass
class GetByDeviceQuery:
    """Query to retrieve monitoring data for a specific device."""
    device_id: str
    user_id: str
    limit: int = 50
    skip: int = 0
