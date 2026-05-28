from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

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

    # App
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8001, env="APP_PORT")
    app_env: str = Field(default="development", env="APP_ENV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
