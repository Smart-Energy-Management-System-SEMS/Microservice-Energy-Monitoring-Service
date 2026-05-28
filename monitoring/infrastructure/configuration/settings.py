from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    service_name: str = Field(default="energy-monitoring-service", env="SERVICE_NAME")
    config_service_url: str = Field(default="http://localhost:8090", env="CONFIG_SERVICE_URL")

    # MongoDB
    mongodb_url: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    mongodb_database: str = Field(default="energy_monitoring_db", env="MONGODB_DATABASE")

    # Kafka
    kafka_bootstrap_servers: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_group_id: str = Field(default="energy-monitoring-group", env="KAFKA_GROUP_ID")
    kafka_topic_reading_ingest: str = Field(default="monitoring.reading.ingest", env="KAFKA_TOPIC_READING_INGEST")
    kafka_topic_anomaly_detected: str = Field(default="analytics.anomaly.detected", env="KAFKA_TOPIC_ANOMALY_DETECTED")
    kafka_topic_alert_created: str = Field(default="monitoring.alert.created", env="KAFKA_TOPIC_ALERT_CREATED")
    kafka_topic_reading_processed: str = Field(default="monitoring.reading.processed", env="KAFKA_TOPIC_READING_PROCESSED")
    kafka_security_protocol: str = Field(default="PLAINTEXT", env="KAFKA_SECURITY_PROTOCOL")
    kafka_sasl_mechanism: str | None = Field(default=None, env="KAFKA_SASL_MECHANISM")
    kafka_sasl_username: str | None = Field(default=None, env="KAFKA_SASL_USERNAME")
    kafka_sasl_password: str | None = Field(default=None, env="KAFKA_SASL_PASSWORD")

    # App
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8001, env="APP_PORT")
    app_env: str = Field(default="development", env="APP_ENV")
    api_base_path: str = Field(default="/api/v1", env="API_BASE_PATH")
    cors_allow_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        env="CORS_ALLOW_ORIGINS",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def apply_remote_config(self, config: dict) -> None:
        """
        Applies runtime config values received from Config Service.
        Missing fields keep local env/default values.
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
            "kafka.topics.alert_created": "kafka_topic_alert_created",
            "kafka.topics.reading_processed": "kafka_topic_reading_processed",
        }
        for source_key, target_attr in mapping.items():
            value = self._get_nested(config, source_key)
            if value is not None:
                setattr(self, target_attr, value)

    @staticmethod
    def _get_nested(data: dict, path: str):
        cursor = data
        for part in path.split("."):
            if not isinstance(cursor, dict) or part not in cursor:
                return None
            cursor = cursor[part]
        return cursor

    def get_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


settings = Settings()
