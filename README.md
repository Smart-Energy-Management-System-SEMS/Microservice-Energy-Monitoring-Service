# Microservice-Energy-Monitoring-Service

Part of the **Smart Energy Management System (SEMS)** - Startup Energix  
Universidad Peruana de Ciencias Aplicadas - Ingenieria de Software - Ciclo 7

---

## Overview

Microservice responsible for **real-time energy consumption monitoring**.  
Collects telemetry from smart meters, stores time-series data in MongoDB,
evaluates business rules to generate alerts, and communicates with other
microservices via Kafka.

The service supports centralized runtime configuration via **Config Service**
(`CONFIG_SERVICE_URL`) with local `.env` fallbacks.

## Architecture

```
DDD + Hexagonal Architecture (Ports & Adapters)
|- Domain Layer       -> Entities, Commands, Queries, Value Objects, Repositories (interfaces), Domain Services
|- Application Layer  -> Command Services (CQRS write), Query Services (CQRS read), Event Handlers, Event Publisher
|- Infrastructure     -> MongoDB (Motor async), Kafka (kafka-python), Config Service client
`- Interfaces         -> FastAPI REST Controllers, Resources (Pydantic), Transforms, ACL
```

## Domain Entities

| Entity | Description |
|---|---|
| `EnergyReading` | Raw telemetry from a smart meter (W, V, A, Hz, kWh) |
| `DeviceConsumption` | Aggregated consumption per device per period |
| `ConsumptionAlert` | Alert when thresholds are exceeded or anomalies detected |
| `EnergyMeter` | Registered IoT smart meter device |

## REST API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/energy-readings` | Record a new reading |
| GET | `/api/v1/energy-readings/user/{user_id}` | Readings by user |
| GET | `/api/v1/energy-readings/device/{device_id}` | Readings by device |
| GET | `/api/v1/energy-readings/range` | Readings by date range |
| GET | `/api/v1/energy-readings/meter/{meter_id}/latest` | Latest reading by meter |
| POST | `/api/v1/device-consumptions` | Record device consumption |
| GET | `/api/v1/device-consumptions/user/{user_id}` | Consumptions by user |
| GET | `/api/v1/device-consumptions/user/{user_id}/top` | Top consuming devices |
| POST | `/api/v1/consumption-alerts` | Create an alert |
| GET | `/api/v1/consumption-alerts/user/{user_id}` | Alerts by user |
| GET | `/api/v1/consumption-alerts/user/{user_id}/unread` | Unread alerts |
| PATCH | `/api/v1/consumption-alerts/{id}/read` | Mark alert as read |
| PATCH | `/api/v1/consumption-alerts/{id}/resolve` | Resolve alert |
| POST | `/api/v1/energy-meters` | Register a smart meter |
| GET | `/api/v1/energy-meters/user/{user_id}` | Meters by user |
| PATCH | `/api/v1/energy-meters/{id}/deactivate` | Deactivate meter |

## Kafka Topics

| Direction | Topic | Description |
|---|---|---|
| Consume | `monitoring.reading.ingest` | IoT telemetry from smart meters |
| Consume | `analytics.anomaly.detected` | Anomalies from Analytics Service |
| Publish | `monitoring.alert.created` | New consumption alert |
| Publish | `monitoring.reading.processed` | Processed energy reading |

## Tech Stack

- **Python 3.12** - **FastAPI** - **Uvicorn**
- **MongoDB** (Motor async driver)
- **Apache Kafka** (kafka-python)
- **Docker** + **Docker Compose**
- **Pydantic v2** + **pydantic-settings**

## Configuration Model

### Variables kept in this microservice (`.env`)

- `SERVICE_NAME`
- `CONFIG_SERVICE_URL`
- `MONGODB_URL` (secret)
- `KAFKA_SASL_USERNAME` (secret, optional)
- `KAFKA_SASL_PASSWORD` (secret, optional)
- `APP_HOST`, `APP_PORT`, `APP_ENV`

### Configuration expected from Config Service

- `app.host`, `app.port`, `app.env`
- `api.base_path`
- `mongodb.database`
- `kafka.bootstrap_servers`
- `kafka.group_id`
- `kafka.security_protocol`
- `kafka.sasl_mechanism`
- `kafka.topics.reading_ingest`
- `kafka.topics.anomaly_detected`
- `kafka.topics.alert_created`
- `kafka.topics.reading_processed`

If Config Service is unavailable, local env/default values are used.

## Running Locally

```bash
# 1. Copy env file
cp .env.example .env

# 2. (Optional) Start local infra
docker-compose up mongodb kafka -d

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the service
python main.py
```

## Running with Docker

```bash
docker-compose up --build
```

API docs: `http://localhost:8001/docs`

## Azure Container Apps

- Store `MONGODB_URL`, `KAFKA_SASL_USERNAME`, `KAFKA_SASL_PASSWORD` as ACA Secrets.
- Inject secrets as environment variables.
- Point `CONFIG_SERVICE_URL` to the internal centralized Config Service URL.
- Keep shared config (topics, bootstrap, group, route base) in Config Service.
