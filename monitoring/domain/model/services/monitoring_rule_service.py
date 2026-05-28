from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert, AlertType, AlertSeverity
from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from typing import Optional
from datetime import datetime


class MonitoringRuleService:
    """
    Domain Service: Encapsulates business rules for evaluating energy readings
    and generating alerts based on configured thresholds.
    """

    DEFAULT_HIGH_POWER_THRESHOLD_W = 2000.0   # 2 kW
    DEFAULT_CRITICAL_POWER_THRESHOLD_W = 5000.0  # 5 kW
    DEFAULT_HIGH_KWH_THRESHOLD = 100.0          # 100 kWh per period

    def evaluate_reading(
        self,
        reading: EnergyReading,
        power_threshold_w: float = DEFAULT_HIGH_POWER_THRESHOLD_W
    ) -> Optional[ConsumptionAlert]:
        """
        Evaluate a single energy reading and return a ConsumptionAlert
        if any rule is violated. Returns None if no alert is needed.
        """
        if reading.power_watts >= self.DEFAULT_CRITICAL_POWER_THRESHOLD_W:
            return ConsumptionAlert(
                user_id=reading.user_id,
                device_id=reading.device_id,
                meter_id=reading.meter_id,
                alert_type=AlertType.HIGH_CONSUMPTION,
                severity=AlertSeverity.CRITICAL,
                threshold_value=self.DEFAULT_CRITICAL_POWER_THRESHOLD_W,
                actual_value=reading.power_watts,
                message=(
                    f"CRITICAL: Device '{reading.device_id}' is consuming "
                    f"{reading.power_watts:.1f}W, exceeding the critical threshold "
                    f"of {self.DEFAULT_CRITICAL_POWER_THRESHOLD_W:.0f}W."
                ),
            )
        elif reading.power_watts >= power_threshold_w:
            return ConsumptionAlert(
                user_id=reading.user_id,
                device_id=reading.device_id,
                meter_id=reading.meter_id,
                alert_type=AlertType.HIGH_CONSUMPTION,
                severity=AlertSeverity.HIGH,
                threshold_value=power_threshold_w,
                actual_value=reading.power_watts,
                message=(
                    f"High consumption detected: Device '{reading.device_id}' is consuming "
                    f"{reading.power_watts:.1f}W, exceeding the threshold of {power_threshold_w:.0f}W."
                ),
            )
        return None

    def evaluate_device_consumption(
        self,
        consumption: DeviceConsumption,
        kwh_threshold: float = DEFAULT_HIGH_KWH_THRESHOLD
    ) -> Optional[ConsumptionAlert]:
        """
        Evaluate aggregated device consumption for the billing period
        and return an alert if total kWh exceeds the threshold.
        """
        if consumption.total_kwh >= kwh_threshold:
            return ConsumptionAlert(
                user_id=consumption.user_id,
                device_id=consumption.device_id,
                meter_id=consumption.meter_id,
                alert_type=AlertType.THRESHOLD_EXCEEDED,
                severity=AlertSeverity.MEDIUM,
                threshold_value=kwh_threshold,
                actual_value=consumption.total_kwh,
                message=(
                    f"Device '{consumption.device_name}' has consumed {consumption.total_kwh:.2f} kWh "
                    f"this period, exceeding the limit of {kwh_threshold:.0f} kWh. "
                    f"Estimated cost: S/. {consumption.cost_estimate_soles:.2f}."
                ),
            )
        return None
