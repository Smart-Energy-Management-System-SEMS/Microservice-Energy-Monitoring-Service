# Energy Monitoring Service

Microservicio Python del proyecto SEMS. Expone endpoints REST con FastAPI, consume/publica eventos en Kafka y usa MongoDB.

## Requisitos

- Python 3.12+
- Docker (opcional para contenedor)

## Variables de entorno

Usa `.env.example` como base. Variables principales para local/Azure:

```env
PORT=8080
CONFIG_SERVICE_URL=
KAFKA_BROKERS=localhost:9092
KAFKA_SECURITY_PROTOCOL=
KAFKA_SASL_MECHANISM=
KAFKA_USERNAME=
KAFKA_PASSWORD=
DATABASE_URL=
MONGODB_URI=
ENVIRONMENT=production
```

Notas:
- En local puedes mantener `KAFKA_BROKERS=localhost:9092`.
- En Azure Container Apps no uses `localhost` para servicios externos (Kafka, Config Service, MongoDB).
- El servicio acepta aliases legacy (`APP_PORT`, `APP_ENV`, `KAFKA_BOOTSTRAP_SERVERS`, `MONGODB_URL`, etc.) para compatibilidad.

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

## Docker

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
5. Configura `CONFIG_SERVICE_URL`, `KAFKA_BROKERS`, `MONGODB_URI` con endpoints reales de Azure/red privada (no `localhost`).

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
