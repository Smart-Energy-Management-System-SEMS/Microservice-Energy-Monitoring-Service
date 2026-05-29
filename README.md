# Energy Monitoring Service

Microservicio Python para el Smart Energy Management System (SEMS). Gestiona lecturas de energía, consumo por dispositivo, alertas de consumo y medidores inteligentes usando DDD + Arquitectura Hexagonal, FastAPI, Motor, MongoDB Atlas y Apache Kafka.

## Stack

- Python 3.11
- FastAPI + Uvicorn (REST framework)
- Motor (driver async para MongoDB)
- MongoDB Atlas mediante `MONGODB_URL`
- Apache Kafka mediante `kafka-python`
- Arquitectura DDD + Hexagonal con capas `monitoring/domain`, `monitoring/application`, `monitoring/infrastructure` y `monitoring/interfaces`

## Variables de entorno

Copia `.env.example` a `.env` y coloca tu cadena real de MongoDB Atlas. No ejecutes el servicio con el placeholder `<usuario>:<password>@<cluster>`, porque las credenciales deben ser reales.

```env
MONGODB_URL=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=SEMS
MONGODB_DATABASE=energy_monitoring_db
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=energy-monitoring-group
KAFKA_TOPIC_READING_INGEST=monitoring.reading.ingest
KAFKA_TOPIC_ANOMALY_DETECTED=analytics.anomaly.detected
KAFKA_TOPIC_ALERT_CREATED=monitoring.alert.created
KAFKA_TOPIC_READING_PROCESSED=monitoring.reading.processed
APP_HOST=0.0.0.0
APP_PORT=8001
APP_ENV=development
```

## Ejecutar localmente

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr el servicio
python main.py
```

El servicio arranca por defecto en:

```
http://localhost:8001/api/v1
```

Documentación interactiva (Swagger UI):

```
http://localhost:8001/docs
```

Health check:

```
GET /api/v1/health
```

Si Kafka no está disponible en local, el servicio lo detecta y continúa sin publicar eventos. Los endpoints REST siguen funcionando con normalidad.

## Docker

El proyecto incluye `Dockerfile`, `.dockerignore` y `docker-compose.yml`.

Construir imagen:

```bash
docker build -t energy-monitoring-service .
```

Ejecutar contenedor usando tus variables locales:

```bash
docker run --env-file .env -p 8001:8001 energy-monitoring-service
```

Ejecutar con Docker Compose (incluye Kafka + Zookeeper):

```bash
docker compose up --build
```

Health check:

```
GET http://localhost:8001/api/v1/health
```

> **Nota:** `.env` no se copia dentro de la imagen y está excluido por `.dockerignore`. Docker Compose lo lee en runtime con `env_file`. La base de datos vive en MongoDB Atlas, por lo que no se levanta ningún contenedor de MongoDB localmente.

## Endpoints REST

### Energy Readings

```
POST   /api/v1/energy-readings
GET    /api/v1/energy-readings/{reading_id}
GET    /api/v1/energy-readings/user/{user_id}
GET    /api/v1/energy-readings/device/{device_id}
GET    /api/v1/energy-readings/range
GET    /api/v1/energy-readings/meter/{meter_id}/latest
```

### Device Consumptions

```
POST   /api/v1/device-consumptions
GET    /api/v1/device-consumptions/{consumption_id}
GET    /api/v1/device-consumptions/user/{user_id}
GET    /api/v1/device-consumptions/user/{user_id}/top
```

### Consumption Alerts

```
POST   /api/v1/consumption-alerts
GET    /api/v1/consumption-alerts/{alert_id}
GET    /api/v1/consumption-alerts/user/{user_id}
GET    /api/v1/consumption-alerts/user/{user_id}/unread
PATCH  /api/v1/consumption-alerts/{alert_id}/read
PATCH  /api/v1/consumption-alerts/{alert_id}/resolve
```

### Energy Meters

```
POST   /api/v1/energy-meters
GET    /api/v1/energy-meters/{meter_id}
GET    /api/v1/energy-meters/user/{user_id}
PATCH  /api/v1/energy-meters/{meter_id}/deactivate
```

### Health

```
GET    /api/v1/health
```

## Valores permitidos

`reading_type`:
- `real_time`, `scheduled`, `on_demand`

`phase`:
- `single`, `three`

`alert_type`:
- `high_consumption`, `anomaly_detected`, `device_always_on`, `threshold_exceeded`, `unusual_pattern`

`severity`:
- `low`, `medium`, `high`, `critical`

`meter_status`:
- `active`, `inactive`, `maintenance`, `error`

## Kafka

El servicio consume y publica eventos JSON en estos tópicos:

| Dirección | Tópico | Descripción |
|---|---|---|
| Consume | `monitoring.reading.ingest` | Telemetría IoT desde el gateway |
| Consume | `analytics.anomaly.detected` | Anomalías detectadas por el Analytics Service |
| Publica | `monitoring.reading.processed` | Lectura procesada y almacenada |
| Publica | `monitoring.alert.created` | Nueva alerta de consumo generada |

Formato base del evento publicado:

```json
{
  "event_type": "EnergyReadingProcessed",
  "reading_id": "64f1a2b3c4d5e6f7a8b9c0d1",
  "user_id": "0c389ba8-99ca-492b-8b7d-86c5056613f6",
  "meter_id": "b9f9a832-4d2a-4a48-95e1-8c14687d16d5",
  "device_id": "3f1a9c72-8b4e-4d2a-9f0c-7e3b5d1a6f82",
  "power_watts": 1850.5,
  "energy_kwh": 1.23,
  "timestamp": "2026-05-26T22:00:00Z",
  "occurred_at": "2026-05-26T22:00:01Z"
}
```

## Ejemplos JSON

### Registrar lectura de energía

```json
{
  "user_id": "0c389ba8-99ca-492b-8b7d-86c5056613f6",
  "meter_id": "b9f9a832-4d2a-4a48-95e1-8c14687d16d5",
  "device_id": "3f1a9c72-8b4e-4d2a-9f0c-7e3b5d1a6f82",
  "power_watts": 1850.5,
  "voltage": 220.0,
  "current": 8.4,
  "frequency": 60.0,
  "energy_kwh": 1.23,
  "timestamp": "2026-05-26T22:00:00Z",
  "reading_type": "real_time",
  "phase": "single"
}
```

### Registrar consumo de dispositivo

```json
{
  "user_id": "0c389ba8-99ca-492b-8b7d-86c5056613f6",
  "device_id": "3f1a9c72-8b4e-4d2a-9f0c-7e3b5d1a6f82",
  "device_name": "Smart Meter Sala",
  "meter_id": "b9f9a832-4d2a-4a48-95e1-8c14687d16d5",
  "total_kwh": 85.4,
  "cost_estimate_soles": 58.07,
  "period_start": "2026-05-01T00:00:00Z",
  "period_end": "2026-05-31T23:59:59Z",
  "peak_power_watts": 3200.0,
  "average_power_watts": 1150.0,
  "reading_count": 1440
}
```

### Crear alerta de consumo

```json
{
  "user_id": "0c389ba8-99ca-492b-8b7d-86c5056613f6",
  "device_id": "3f1a9c72-8b4e-4d2a-9f0c-7e3b5d1a6f82",
  "meter_id": "b9f9a832-4d2a-4a48-95e1-8c14687d16d5",
  "alert_type": "high_consumption",
  "severity": "high",
  "threshold_value": 2000.0,
  "actual_value": 3200.0,
  "message": "Consumo elevado detectado en el medidor de sala"
}
```

### Registrar medidor inteligente

```json
{
  "user_id": "0c389ba8-99ca-492b-8b7d-86c5056613f6",
  "meter_serial": "METER-UPC-001",
  "model": "Pro 3EM",
  "brand": "Shelly",
  "location": "Sala principal",
  "firmware_version": "1.0.0",
  "max_power_watts": 10000.0
}
```

## Reglas de dominio implementadas

- No se registra una lectura sin `user_id`, `meter_id`, `device_id`, `power_watts` ni `timestamp`.
- La potencia en vatios, el voltaje y la corriente no pueden ser negativos.
- La frecuencia debe estar entre 45 y 65 Hz.
- Se genera una alerta automática si `power_watts` supera 2000 W (HIGH) o 5000 W (CRITICAL).
- Se genera una alerta si el consumo acumulado del período supera 100 kWh.
- Un medidor con estado `inactive` no acepta nuevas lecturas.
- El serial del medidor (`meter_serial`) es único por usuario.
- Los controllers no contienen lógica de negocio; delegan a command/query services.
- Los repositorios son interfaces abstractas; las implementaciones MongoDB están en la capa de infraestructura.