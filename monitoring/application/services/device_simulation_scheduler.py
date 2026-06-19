import asyncio
import logging
from dataclasses import dataclass

from monitoring.application.commandservices.energy_simulation_command_service import EnergySimulationCommandService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SimulatedDeviceRegistration:
    user_id: str
    device_id: str
    device_type: str
    status: str


class DeviceSimulationScheduler:
    """Keeps per-device simulation loops running in memory."""

    def __init__(
        self,
        simulation_command_service: EnergySimulationCommandService,
        interval_seconds: int = 3600,
    ):
        self._simulation_command_service = simulation_command_service
        self._interval_seconds = max(1, interval_seconds)
        self._tasks: dict[str, asyncio.Task] = {}
        self._devices: dict[str, SimulatedDeviceRegistration] = {}

    async def activate_device(self, registration: SimulatedDeviceRegistration) -> None:
        """Start a simulation loop for the device if it is active."""
        if registration.status.upper() != "ACTIVE":
            logger.info(
                "Ignoring device.registered for device_id=%s because status=%s",
                registration.device_id,
                registration.status,
            )
            return

        self._devices[registration.device_id] = registration
        running_task = self._tasks.get(registration.device_id)
        if running_task and not running_task.done():
            logger.info("Simulation already active for device_id=%s", registration.device_id)
            return

        task = asyncio.create_task(
            self._run_device_loop(registration),
            name=f"device-simulation-{registration.device_id}",
        )
        self._tasks[registration.device_id] = task
        task.add_done_callback(lambda completed, device_id=registration.device_id: self._cleanup_task(device_id, completed))
        logger.info(
            "Activated simulation for device_id=%s interval=%ss",
            registration.device_id,
            self._interval_seconds,
        )

    async def stop_all(self) -> None:
        """Cancel all running simulation loops gracefully."""
        tasks = [task for task in self._tasks.values() if not task.done()]
        if not tasks:
            return

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self._tasks.clear()
        logger.info("Stopped %s device simulation task(s)", len(tasks))

    async def _run_device_loop(self, registration: SimulatedDeviceRegistration) -> None:
        # Generate one reading immediately so a new device produces data right away.
        while True:
            try:
                reading, _, estimated_cost = await self._simulation_command_service.generate_reading(
                    user_id=registration.user_id,
                    device_id=registration.device_id,
                    device_type=registration.device_type,
                )
                logger.info(
                    "Simulated reading generated for device_id=%s type=%s power_watts=%.2f energy_kwh=%.3f estimated_cost=%.2f",
                    registration.device_id,
                    registration.device_type,
                    reading.power_watts,
                    reading.energy_kwh,
                    estimated_cost,
                )
                await asyncio.sleep(self._interval_seconds)
            except asyncio.CancelledError:
                logger.info("Simulation loop cancelled for device_id=%s", registration.device_id)
                raise
            except Exception:
                logger.exception("Simulation loop failed for device_id=%s", registration.device_id)
                await asyncio.sleep(min(self._interval_seconds, 30))

    def _cleanup_task(self, device_id: str, task: asyncio.Task) -> None:
        current = self._tasks.get(device_id)
        if current is task:
            self._tasks.pop(device_id, None)
