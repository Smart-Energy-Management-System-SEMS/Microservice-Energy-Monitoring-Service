"""
Dependency injection container for FastAPI.
Wires repositories, services and event publisher together.
"""
from functools import lru_cache
from monitoring.infrastructure.persistence.mongodb.configuration.mongodb_client import MongoDBClient
from monitoring.infrastructure.persistence.mongodb.repositories.energy_reading_mongodb_repository import EnergyReadingMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.repositories.device_consumption_mongodb_repository import DeviceConsumptionMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.repositories.consumption_alert_mongodb_repository import ConsumptionAlertMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.repositories.energy_meter_mongodb_repository import EnergyMeterMongoDBRepository
from monitoring.domain.model.services.monitoring_rule_service import MonitoringRuleService
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher
from monitoring.application.commandservices.energy_reading_command_service import EnergyReadingCommandService
from monitoring.application.commandservices.device_consumption_command_service import DeviceConsumptionCommandService
from monitoring.application.commandservices.consumption_alert_command_service import ConsumptionAlertCommandService
from monitoring.application.commandservices.energy_meter_command_service import EnergyMeterCommandService
from monitoring.application.queryservices.energy_reading_query_service import EnergyReadingQueryService
from monitoring.application.queryservices.device_consumption_query_service import DeviceConsumptionQueryService
from monitoring.application.queryservices.consumption_alert_query_service import ConsumptionAlertQueryService
from monitoring.application.queryservices.energy_meter_query_service import EnergyMeterQueryService


def get_db():
    return MongoDBClient.get_database()


# Repositories
def get_reading_repo():
    return EnergyReadingMongoDBRepository(get_db())


def get_consumption_repo():
    return DeviceConsumptionMongoDBRepository(get_db())


def get_alert_repo():
    return ConsumptionAlertMongoDBRepository(get_db())


def get_meter_repo():
    return EnergyMeterMongoDBRepository(get_db())


# Domain services
def get_rule_service():
    return MonitoringRuleService()


def get_event_publisher():
    return MonitoringEventPublisher()


# Command services
def get_reading_command_service():
    return EnergyReadingCommandService(get_reading_repo(), get_rule_service(), get_event_publisher())


def get_consumption_command_service():
    return DeviceConsumptionCommandService(get_consumption_repo(), get_alert_repo(), get_rule_service(), get_event_publisher())


def get_alert_command_service():
    return ConsumptionAlertCommandService(get_alert_repo(), get_event_publisher())


def get_meter_command_service():
    return EnergyMeterCommandService(get_meter_repo())


# Query services
def get_reading_query_service():
    return EnergyReadingQueryService(get_reading_repo())


def get_consumption_query_service():
    return DeviceConsumptionQueryService(get_consumption_repo())


def get_alert_query_service():
    return ConsumptionAlertQueryService(get_alert_repo())


def get_meter_query_service():
    return EnergyMeterQueryService(get_meter_repo())
