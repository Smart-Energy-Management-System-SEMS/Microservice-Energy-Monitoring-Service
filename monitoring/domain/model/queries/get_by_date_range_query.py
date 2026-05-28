from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetByDateRangeQuery:
    """Query to retrieve monitoring data within a date/time range."""
    user_id: str
    start_date: datetime
    end_date: datetime
    device_id: str = None
    limit: int = 100
    skip: int = 0
