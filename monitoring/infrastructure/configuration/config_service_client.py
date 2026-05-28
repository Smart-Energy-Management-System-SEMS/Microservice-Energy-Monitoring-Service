import logging
from typing import Any, Dict
import httpx

from monitoring.infrastructure.configuration.settings import settings

logger = logging.getLogger(__name__)


class ConfigServiceClient:
    """Client for retrieving service configuration from centralized Config Service."""

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 5.0):
        self._base_url = (base_url or settings.config_service_url).rstrip("/")
        self._timeout = timeout_seconds

    async def get_service_config(self, service_name: str) -> Dict[str, Any]:
        endpoint = f"{self._base_url}/api/v1/config/{service_name}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Config Service response must be a JSON object.")
            return payload

    async def get_services_config(self) -> Dict[str, Any]:
        endpoint = f"{self._base_url}/api/v1/config/services"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Config Service response must be a JSON object.")
            return payload

    async def get_kafka_config(self) -> Dict[str, Any]:
        endpoint = f"{self._base_url}/api/v1/config/kafka"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Config Service response must be a JSON object.")
            return payload

    async def load_into_settings(self, service_name: str) -> None:
        try:
            remote = await self.get_service_config(service_name)
            settings.apply_remote_config(remote)
            logger.info("Remote configuration loaded from Config Service.")
        except Exception as exc:
            logger.warning(
                "Config Service unavailable or invalid response. Using local env/default settings. error=%s",
                exc,
            )
