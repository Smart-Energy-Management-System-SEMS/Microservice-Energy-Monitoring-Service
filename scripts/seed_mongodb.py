import asyncio
import random
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

import motor.motor_asyncio
from bson import ObjectId

MONGODB_URL      = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "energy_monitoring_db")

USER_IDS   = ["user_001", "user_002", "user_003"]
METER_IDS  = [str(ObjectId()) for _ in range(6)]
DEVICE_IDS = [str(ObjectId()) for _ in range(9)]

DEVICE_NAMES = [
    "Aire Acondicionado", "Refrigeradora", "Lavadora",
    "Televisor 4K",       "Computadora",   "Microondas",
    "Iluminacion LED",    "Calefactor",    "Bomba de agua",
]

METER_SERIALS = [
    "SM-2024-001A", "SM-2024-001B",
    "SM-2024-002A", "SM-2024-002B",
    "SM-2024-003A", "SM-2024-003B",
]

BRANDS   = ["Schneider Electric", "ABB", "Siemens", "Legrand"]
MODELS   = ["iEM3155", "EQ-DIN", "PAC3200", "DMG800"]
LOCS     = ["Sala principal", "Cuarto de maquinas", "Cocina", "Oficina", "Sotano", "Terraza"]
STATUSES = ["active", "active", "active", "inactive", "maintenance"]

ALERT_TYPES = [
    "high_consumption", "anomaly_detected",
    "device_always_on", "threshold_exceeded", "unusual_pattern",
]
SEVERITIES = ["low", "medium", "high", "critical"]


def make_meter(index: int) -> dict:
    user_idx   = index // 2
    user_id    = USER_IDS[user_idx]
    now        = datetime.utcnow()
    registered = now - timedelta(days=random.randint(30, 365))
    return {
        "_id":              ObjectId(METER_IDS[index]),
        "user_id":          user_id,
        "meter_serial":     METER_SERIALS[index],
        "model":            random.choice(MODELS),
        "brand":            random.choice(BRANDS),
        "location":         LOCS[index],
        "status":           random.choice(STATUSES),
        "firmware_version": f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "max_power_watts":  random.choice([5000.0, 8000.0, 10000.0, 15000.0]),
        "registered_at":    registered,
        "last_seen_at":     now - timedelta(minutes=random.randint(1, 120)),
        "updated_at":       now - timedelta(hours=random.randint(1, 48)),
    }


def make_readings(meter_idx: int, count: int = 50) -> list:
    user_idx  = meter_idx // 2
    user_id   = USER_IDS[user_idx]
    meter_id  = METER_IDS[meter_idx]
    device_id = DEVICE_IDS[user_idx * 3 + (meter_idx % 3)]
    docs      = []
    base_time = datetime.utcnow() - timedelta(hours=count)

    for i in range(count):
        power    = round(random.uniform(50, 3500), 2)
        voltage  = round(random.uniform(215, 225), 2)
        current  = round(power / voltage, 4)
        freq     = round(random.uniform(59.8, 60.2), 2)
        energy   = round(power / 1000 * random.uniform(0.01, 0.1), 6)
        ts       = base_time + timedelta(hours=i, minutes=random.randint(0, 59))
        docs.append({
            "_id":          ObjectId(),
            "user_id":      user_id,
            "meter_id":     meter_id,
            "device_id":    device_id,
            "power_watts":  power,
            "voltage":      voltage,
            "current":      current,
            "frequency":    freq,
            "energy_kwh":   energy,
            "timestamp":    ts,
            "reading_type": random.choice(["real_time", "scheduled", "on_demand"]),
            "phase":        random.choice(["single", "three"]),
            "created_at":   ts,
        })
    return docs


def make_device_consumptions() -> list:
    docs = []
    now  = datetime.utcnow()
    for ui, user_id in enumerate(USER_IDS):
        for di in range(3):
            device_idx   = ui * 3 + di
            device_id    = DEVICE_IDS[device_idx]
            device_name  = DEVICE_NAMES[device_idx]
            meter_id     = METER_IDS[ui * 2]
            period_start = now - timedelta(days=30)
            period_end   = now
            total_kwh    = round(random.uniform(5, 300), 4)
            avg_power    = round(random.uniform(50, 2000), 2)
            peak_power   = round(avg_power * random.uniform(1.2, 2.5), 2)
            readings_n   = random.randint(200, 1500)
            cost         = round(total_kwh * 0.68, 4)
            docs.append({
                "_id":                  ObjectId(),
                "user_id":              user_id,
                "device_id":            device_id,
                "device_name":          device_name,
                "meter_id":             meter_id,
                "total_kwh":            total_kwh,
                "cost_estimate_soles":  cost,
                "period_start":         period_start,
                "period_end":           period_end,
                "peak_power_watts":     peak_power,
                "average_power_watts":  avg_power,
                "reading_count":        readings_n,
                "created_at":           period_start,
                "updated_at":           now,
            })
    return docs


def make_alerts() -> list:
    docs = []
    now  = datetime.utcnow()
    for ui, user_id in enumerate(USER_IDS):
        for _ in range(random.randint(4, 8)):
            device_idx  = random.randint(0, 2)
            device_id   = DEVICE_IDS[ui * 3 + device_idx]
            meter_id    = METER_IDS[ui * 2]
            alert_type  = random.choice(ALERT_TYPES)
            severity    = random.choice(SEVERITIES)
            threshold   = round(random.uniform(1000, 3000), 2)
            actual      = round(threshold * random.uniform(1.05, 2.0), 2)
            is_resolved = random.random() > 0.4
            created_at  = now - timedelta(hours=random.randint(1, 72))
            resolved_at = (created_at + timedelta(hours=random.randint(1, 12))
                           if is_resolved else None)
            messages = {
                "high_consumption":   f"Consumo elevado: {actual:.1f} W supera el umbral de {threshold:.1f} W",
                "anomaly_detected":   f"Patron anomalo detectado. Potencia: {actual:.1f} W",
                "device_always_on":   f"Dispositivo encendido mas de 24 h ({actual:.1f} W)",
                "threshold_exceeded": f"Limite superado: {actual:.1f} W > {threshold:.1f} W",
                "unusual_pattern":    f"Consumo fuera del rango normal a las {created_at.strftime('%H:%M')}",
            }
            docs.append({
                "_id":             ObjectId(),
                "user_id":         user_id,
                "device_id":       device_id,
                "meter_id":        meter_id,
                "alert_type":      alert_type,
                "severity":        severity,
                "threshold_value": threshold,
                "actual_value":    actual,
                "message":         messages[alert_type],
                "is_read":         random.random() > 0.5,
                "is_resolved":     is_resolved,
                "created_at":      created_at,
                "resolved_at":     resolved_at,
            })
    return docs


async def seed():
    print(f"DB: {MONGODB_DATABASE}")
    print(f"URL: {MONGODB_URL[:55]}...\n")

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    db     = client[MONGODB_DATABASE]

    cols = ["energy_meters", "energy_readings", "device_consumptions", "consumption_alerts"]
    for col in cols:
        result = await db[col].delete_many({})
        print(f"Deleted {result.deleted_count} from {col}")

    print()

    meters = [make_meter(i) for i in range(6)]
    await db["energy_meters"].insert_many(meters)
    print(f"energy_meters        -> {len(meters)}")

    all_readings = []
    for i in range(6):
        all_readings.extend(make_readings(i, count=50))
    await db["energy_readings"].insert_many(all_readings)
    print(f"energy_readings      -> {len(all_readings)}")

    consumptions = make_device_consumptions()
    await db["device_consumptions"].insert_many(consumptions)
    print(f"device_consumptions  -> {len(consumptions)}")

    alerts = make_alerts()
    await db["consumption_alerts"].insert_many(alerts)
    print(f"consumption_alerts   -> {len(alerts)}")

    await db["energy_meters"].create_index("user_id")
    await db["energy_meters"].create_index("meter_serial", unique=True)
    await db["energy_readings"].create_index([("user_id", 1), ("timestamp", -1)])
    await db["energy_readings"].create_index("meter_id")
    await db["device_consumptions"].create_index([("user_id", 1), ("device_id", 1)])
    await db["consumption_alerts"].create_index([("user_id", 1), ("created_at", -1)])
    await db["consumption_alerts"].create_index("is_resolved")

    client.close()
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(seed())
