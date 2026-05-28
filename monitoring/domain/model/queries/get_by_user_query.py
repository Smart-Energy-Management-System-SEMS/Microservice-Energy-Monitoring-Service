from dataclasses import dataclass


@dataclass
class GetByUserQuery:
    """Query to retrieve monitoring data by user ID."""
    user_id: str
    limit: int = 50
    skip: int = 0
