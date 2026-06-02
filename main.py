import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from monitoring.infrastructure.configuration.settings import settings
from monitoring.infrastructure.configuration.config_service_client import ConfigServiceClient
from monitoring.infrastructure.persistence.mongodb.configuration.mongodb_client import MongoDBClient
from monitoring.infrastructure.messaging.kafka.kafka_consumer import KafkaConsumer
from monitoring.infrastructure.messaging.kafka.kafka_producer import KafkaProducer
from monitoring.application.eventhandlers.monitoring_event_handler import MonitoringEventHandler

from monitoring.interfaces.rest.controllers.health_controller import router as health_router
from monitoring.interfaces.rest.controllers.energy_reading_controller import router as reading_router
from monitoring.interfaces.rest.controllers.energy_simulation_controller import router as energy_simulation_router
from monitoring.interfaces.rest.controllers.device_consumption_controller import router as consumption_router
from monitoring.interfaces.rest.controllers.consumption_alert_controller import router as alert_router
from monitoring.interfaces.rest.controllers.energy_meter_controller import router as meter_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

kafka_consumer = KafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle management."""
    logger.info("=== Microservice-Energy-Monitoring-Service starting up ===")

    # Load non-secret distributed settings from Config Service
    await ConfigServiceClient().load_into_settings(settings.service_name)

    # Initialize MongoDB connection (lazy, validates on first use)
    MongoDBClient.get_database()
    logger.info("MongoDB client initialized.")

    # Register and start Kafka consumer
    event_handler = MonitoringEventHandler(kafka_consumer)
    event_handler.register_handlers()
    kafka_consumer.start()
    logger.info("Kafka consumer started.")

    yield

    # Shutdown
    kafka_consumer.stop()
    KafkaProducer.close()
    await MongoDBClient.close()
    logger.info("=== Microservice-Energy-Monitoring-Service shut down ===")


app = FastAPI(
    title="Microservice-Energy-Monitoring-Service",
    description=(
        "SEMS - Smart Energy Management System\n\n"
        "Microservice responsible for collecting, storing, and exposing "
        "real-time energy consumption data from smart meters. "
        "Built with DDD + Hexagonal Architecture, FastAPI, MongoDB and Kafka."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router, prefix=settings.api_base_path)
app.include_router(energy_simulation_router, prefix=settings.api_base_path)
app.include_router(reading_router, prefix=settings.api_base_path)
app.include_router(consumption_router, prefix=settings.api_base_path)
app.include_router(alert_router, prefix=settings.api_base_path)
app.include_router(meter_router, prefix=settings.api_base_path)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
        log_level="info",
    )
