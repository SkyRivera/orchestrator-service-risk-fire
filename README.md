````markdown
# Orchestrator Service (BFF) - Risk Fire Monitoring

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3121/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Servicio Orquestador (Backend for Frontend) para la evaluación de riesgo de incendios forestales. Coordina la descarga de imágenes desde `media-api`, consulta concurrentemente a `nubosity-api`, `vegetation-api` y `telemetry-api`, envía la información consolidada a `risk-fire-api`, y evalúa el resultado contra un motor de reglas dinámicas en PostgreSQL.

## 🚀 Características Principales

- **Orquestación Asíncrona:** Uso de `asyncio.gather` para consultar 3 APIs en paralelo.
- **Integración con Media API:** Descarga y envío de binarios de imágenes sin almacenamiento local.
- **Motor de Reglas Dinámicas:** Decisiones operativas (semáforo, medidas) almacenadas en BD y cacheadas en memoria.
- **Alta Resiliencia:** Manejo de _timeouts_, reintentos con backoff exponencial y fallbacks para telemetría.
- **Trazabilidad:** Inyección de `Correlation ID` en todas las peticiones y logs estructurados.
- **Auditoría Completa:** Persistencia de cada evaluación (éxitos y fallos) en PostgreSQL.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.12.1
- **Framework:** FastAPI 0.141.1
- **Validación:** Pydantic v2
- **ORM:** SQLAlchemy 2.x (async) + asyncpg
- **Base de Datos:** PostgreSQL 18.6
- **Cliente HTTP:** httpx

## 📋 Requisitos Previos

- Python 3.12+
- PostgreSQL 18.6+ (o Docker)
- Acceso a las APIs externas (`media`, `nubosity`, `vegetation`, `telemetry`, `risk-fire`).

## ⚙️ Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-org/orchestrator-service-risk-fire.git
   cd orchestrator-service-risk-fire
   ```
````
