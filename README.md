# Energy Monitoring Service

Microservicio Python del proyecto SEMS. Expone endpoints REST con FastAPI, consume/publica eventos en Kafka y usa MongoDB.

Incluye una simulacion interna para EOS IoT y Plus Energia. No hace llamadas reales a sistemas externos: genera telemetria por `device_id`, guarda lecturas en MongoDB y publica eventos Kafka.

## Requisitos

- Python 3.12+
- Docker (opcional para contenedor)

## Variables de entorno

Usa `.env.example` como base. Variables principales para local/Docker/Azure:

```env
PORT=8080
CONFIG_SERVICE_URL=
KAFKA_BROKERS=kafka:9092
KAFKA_SECURITY_PROTOCOL=
KAFKA_SASL_MECHANISM=
KAFKA_USERNAME=
KAFKA_PASSWORD=
DATABASE_URL=
MONGODB_URI=
ENVIRONMENT=production
KAFKA_TOPIC_DEVICE_EVENTS=device.events
KAFKA_TOPIC_ENERGY_EVENTS=energy.events
KAFKA_TOPIC_ANALYTICS_EVENTS=analytics.events
KAFKA_TOPIC_ALERTS_EVENTS=alerts.events
KAFKA_ENABLE_TOPIC_INIT=true
```

Notas:
- Si corres este micro dentro de `docker-compose`, usa `KAFKA_BROKERS=kafka:9092`.
- Para Azure Event Hubs usa `KAFKA_BROKERS=<namespace>.servicebus.windows.net:9093`, `KAFKA_SECURITY_PROTOCOL=SASL_SSL`, `KAFKA_SASL_MECHANISM=PLAIN`, `KAFKA_USERNAME=$ConnectionString` y `KAFKA_ENABLE_TOPIC_INIT=false`.
- Este micro publica `energy.reading.created` y `energy.consumption.recorded` dentro de `energy.events`.
- Este micro publica `energy.reading.processed` dentro de `energy.events` y `alert.created` dentro de `alerts.events`.
- Consume `device.events`, `energy.events` y `analytics.events`, filtrando por `eventType`.
- El servicio acepta aliases legacy (`APP_PORT`, `APP_ENV`, `KAFKA_BOOTSTRAP_SERVERS`, `MONGODB_URL`, etc.) para compatibilidad.
- Al arrancar, el servicio intenta crear automaticamente los topics Kafka que necesita.

## Ejecucion local

```bash
cp .env.example .env
pip install -r requirements.txt
python main.py
```

Base URL local:

```text
http://localhost:8080
```

Health check:

```text
GET /api/v1/health
```

## Endpoints de simulacion

Generar lectura simulada:

```http
POST /api/v1/energy/simulation/readings
Content-Type: application/json

{
  "user_id": "user_001",
  "device_id": "device_001"
}
```

Consultar consumo actual por dispositivo:

```text
GET /api/v1/energy/devices/device_001/consumption/current
```

Consultar historial por dispositivo:

```text
GET /api/v1/energy/devices/device_001/consumption/history
```

Consultar precio actual:

```text
GET /api/v1/energy/pricing/current
```

Respuesta esperada del pricing mock:

```json
{
  "provider": "Plus Energia",
  "price_per_kwh": 0.82,
  "currency": "PEN"
}
```

Evento Kafka publicado al generar una lectura:

```json
{
  "eventId": "uuid",
  "eventType": "energy.consumption.recorded",
  "occurredAt": "2026-06-12T22:30:00Z",
  "user_id": "user_001",
  "device_id": "device_001",
  "reading_id": "reading_001",
  "meter_id": "sim-meter-device_001",
  "power_watts": 850,
  "energy_kwh": 1.25,
  "estimated_cost": 0.94,
  "currency": "PEN",
  "timestamp": "2026-06-02T20:15:00+00:00",
  "data": {
    "user_id": "user_001",
    "device_id": "device_001",
    "reading_id": "reading_001",
    "meter_id": "sim-meter-device_001",
    "power_watts": 850,
    "energy_kwh": 1.25,
    "estimated_cost": 0.94,
    "currency": "PEN",
    "timestamp": "2026-06-02T20:15:00+00:00"
  }
}
```

## Docker

Con `docker-compose.yml`:

```bash
docker compose up -d kafka zookeeper kafka-init
```

El compose deja Kafka accesible por `kafka:9092` dentro de la red Docker y anuncia `host.docker.internal:29092` como listener externo.

Ademas, el micro intenta asegurar estos topics al iniciar:
- `device.events`
- `energy.events`
- `analytics.events`
- `alerts.events`

Construir imagen:

```bash
docker build -t energy-monitoring-service:latest .
```

Ejecutar contenedor:

```bash
docker run --rm -p 8080:8080 --env-file .env energy-monitoring-service:latest
```

## Azure Container Apps

1. Publica la imagen en ACR (o Docker Hub).
2. Crea/actualiza la Container App usando esa imagen.
3. Configura variables de entorno y secretos en la Container App.
4. Define `PORT=8080` en la app.
5. Configura `CONFIG_SERVICE_URL`, `KAFKA_BROKERS`, `MONGODB_URI` con endpoints reales de Azure/red privada.

Ejemplo de despliegue (CLI):

```bash
az containerapp create \
  --name energy-monitoring-service \
  --resource-group <resource-group> \
  --environment <aca-environment> \
  --image <registry>/energy-monitoring-service:latest \
  --target-port 8080 \
  --ingress external \
  --env-vars PORT=8080 ENVIRONMENT=production CONFIG_SERVICE_URL=<config-service-url> KAFKA_BROKERS=<kafka-brokers> KAFKA_SECURITY_PROTOCOL=<protocol> KAFKA_SASL_MECHANISM=<mechanism> MONGODB_URI=<mongodb-uri>
```

Si manejas credenciales sensibles, usa secretos de Azure Container Apps y referencia esos secretos desde variables de entorno.
