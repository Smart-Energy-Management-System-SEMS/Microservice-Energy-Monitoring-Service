# Infrastructure layer: all the app configuration in one place.
# Values come from environment variables (or defaults if they are missing).
import os

from pydantic_settings import BaseSettings
from pydantic import AliasChoices, Field


class Settings(BaseSettings):
    """All the settings the app needs (database, Kafka, server, etc.)."""

    service_name: str = Field(default="energy-monitoring-service", env="SERVICE_NAME")
    config_service_url: str = Field(default="", env="CONFIG_SERVICE_URL")

    # MongoDB
    mongodb_url: str = Field(
        default="mongodb://localhost:27017",
        validation_alias=AliasChoices("MONGODB_URL", "MONGODB_URI", "DATABASE_URL"),
    )
    mongodb_database: str = Field(default="energy_monitoring_db", env="MONGODB_DATABASE")

    # Kafka
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        validation_alias=AliasChoices("KAFKA_BOOTSTRAP_SERVERS", "KAFKA_BROKERS"),
    )
    kafka_group_id: str = Field(default="energy-monitoring-group", env="KAFKA_GROUP_ID")
    kafka_topic_reading_ingest: str = Field(
        default="monitoring.reading.ingest",
        validation_alias=AliasChoices(
            "KAFKA_TOPIC_MONITORING_READING_INGEST",
            "KAFKA_TOPIC_READING_INGEST",
        ),
    )
    kafka_topic_anomaly_detected: str = Field(
        default="analytics.anomaly.detected",
        validation_alias=AliasChoices(
            "KAFKA_TOPIC_ANALYTICS_ANOMALY_DETECTED",
            "KAFKA_TOPIC_ANOMALY_DETECTED",
        ),
    )
    kafka_topic_device_registered: str = Field(
        default="device.registered",
        validation_alias=AliasChoices(
            "KAFKA_TOPIC_DEVICE_REGISTERED",
        ),
    )
    kafka_topic_energy_consumption_recorded: str = Field(
        default="energy.consumption.recorded",
        validation_alias=AliasChoices("KAFKA_TOPIC_ENERGY_CONSUMPTION_RECORDED"),
    )
    kafka_topic_alert_created: str = Field(
        default="monitoring.alert.created",
        validation_alias=AliasChoices(
            "KAFKA_TOPIC_MONITORING_ALERT_CREATED",
            "KAFKA_TOPIC_ALERT_CREATED",
        ),
    )
    kafka_topic_reading_processed: str = Field(
        default="monitoring.reading.processed",
        validation_alias=AliasChoices(
            "KAFKA_TOPIC_MONITORING_READING_PROCESSED",
            "KAFKA_TOPIC_READING_PROCESSED",
        ),
    )
    kafka_topic_energy_reading_created: str = Field(
        default="energy.reading.created",
        env="KAFKA_TOPIC_ENERGY_READING_CREATED",
    )
    kafka_security_protocol: str = Field(default="PLAINTEXT", env="KAFKA_SECURITY_PROTOCOL")
    kafka_sasl_mechanism: str | None = Field(default=None, env="KAFKA_SASL_MECHANISM")
    kafka_sasl_username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("KAFKA_SASL_USERNAME", "KAFKA_USERNAME"),
    )
    kafka_sasl_password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("KAFKA_SASL_PASSWORD", "KAFKA_PASSWORD"),
    )

    # App
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8080, validation_alias=AliasChoices("PORT", "APP_PORT"))
    app_env: str = Field(default="development", validation_alias=AliasChoices("APP_ENV", "ENVIRONMENT"))
    api_base_path: str = Field(default="/api/v1", env="API_BASE_PATH")
    device_simulation_interval_seconds: int = Field(
        default=3600,
        validation_alias=AliasChoices("DEVICE_SIMULATION_INTERVAL_SECONDS"),
    )
    cors_allow_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        env="CORS_ALLOW_ORIGINS",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def apply_remote_config(self, config: dict) -> None:
        """Update settings with values sent by the Config Service.

        Rule: if a real environment variable exists, we keep it and ignore
        the remote value (the local environment always wins).
        """
        mapping = {
            "app.host": "app_host",
            "app.port": "app_port",
            "app.env": "app_env",
            "api.base_path": "api_base_path",
            "mongodb.database": "mongodb_database",
            "kafka.bootstrap_servers": "kafka_bootstrap_servers",
            "kafka.group_id": "kafka_group_id",
            "kafka.security_protocol": "kafka_security_protocol",
            "kafka.sasl_mechanism": "kafka_sasl_mechanism",
            "kafka.topics.reading_ingest": "kafka_topic_reading_ingest",
            "kafka.topics.anomaly_detected": "kafka_topic_anomaly_detected",
            "kafka.topics.device_registered": "kafka_topic_device_registered",
            "kafka.topics.energy_consumption_recorded": "kafka_topic_energy_consumption_recorded",
            "kafka.topics.alert_created": "kafka_topic_alert_created",
            "kafka.topics.reading_processed": "kafka_topic_reading_processed",
            "kafka.topics.energy_reading_created": "kafka_topic_energy_reading_created",
        }
        env_by_attr = {
            "app_host": ("APP_HOST",),
            "app_port": ("PORT", "APP_PORT"),
            "app_env": ("APP_ENV", "ENVIRONMENT"),
            "api_base_path": ("API_BASE_PATH",),
            "mongodb_database": ("MONGODB_DATABASE",),
            "kafka_bootstrap_servers": ("KAFKA_BROKERS", "KAFKA_BOOTSTRAP_SERVERS"),
            "kafka_group_id": ("KAFKA_GROUP_ID",),
            "kafka_security_protocol": ("KAFKA_SECURITY_PROTOCOL",),
            "kafka_sasl_mechanism": ("KAFKA_SASL_MECHANISM",),
            "kafka_topic_reading_ingest": (
                "KAFKA_TOPIC_MONITORING_READING_INGEST",
                "KAFKA_TOPIC_READING_INGEST",
            ),
            "kafka_topic_anomaly_detected": (
                "KAFKA_TOPIC_ANALYTICS_ANOMALY_DETECTED",
                "KAFKA_TOPIC_ANOMALY_DETECTED",
            ),
            "kafka_topic_device_registered": ("KAFKA_TOPIC_DEVICE_REGISTERED",),
            "kafka_topic_energy_consumption_recorded": (
                "KAFKA_TOPIC_ENERGY_CONSUMPTION_RECORDED",
            ),
            "kafka_topic_alert_created": (
                "KAFKA_TOPIC_MONITORING_ALERT_CREATED",
                "KAFKA_TOPIC_ALERT_CREATED",
            ),
            "kafka_topic_reading_processed": (
                "KAFKA_TOPIC_MONITORING_READING_PROCESSED",
                "KAFKA_TOPIC_READING_PROCESSED",
            ),
            "kafka_topic_energy_reading_created": ("KAFKA_TOPIC_ENERGY_READING_CREATED",),
        }
        for source_key, target_attr in mapping.items():
            env_names = env_by_attr.get(target_attr, ())
            if any(os.getenv(name) not in (None, "") for name in env_names):
                continue
            value = self._get_nested(config, source_key)
            if value is not None:
                setattr(self, target_attr, value)

    @staticmethod
    def _get_nested(data: dict, path: str):
        # Read a value from a nested dict using a dotted path like "kafka.group_id".
        cursor = data
        for part in path.split("."):
            if not isinstance(cursor, dict) or part not in cursor:
                return None
            cursor = cursor[part]
        return cursor

    def get_cors_origins(self) -> list[str]:
        """Turn the comma-separated CORS string into a clean list of URLs."""
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]

    def get_kafka_bootstrap_servers(self) -> list[str]:
        return [server.strip() for server in self.kafka_bootstrap_servers.split(",") if server.strip()]

    def get_kafka_topics(self) -> list[str]:
        topics = [
            self.kafka_topic_reading_ingest,
            self.kafka_topic_anomaly_detected,
            self.kafka_topic_device_registered,
            self.kafka_topic_energy_consumption_recorded,
            self.kafka_topic_alert_created,
            self.kafka_topic_reading_processed,
            self.kafka_topic_energy_reading_created,
        ]
        return list(dict.fromkeys(topic for topic in topics if topic))


settings = Settings()
