import asyncio
from app.infrastructure.persistence.database import AsyncSessionLocal
from app.infrastructure.persistence.models.rule import RiskRule
from sqlalchemy import select

DEFAULT_RULES = [
    {
        "risk_category": "Riesgo bajo",
        "estatus": "Normal",
        "semaforo": "Verde",
        "monitoreo": "Monitoreo rutinario cada 24 horas",
        "medidas": "Sin restricciones. Actividades normales.",
        "vigilancia": "Patrullaje estándar",
        "prevencion": "Mantenimiento preventivo de equipos"
    },
    {
        "risk_category": "Riesgo medio",
        "estatus": "Alerta Amarilla",
        "semaforo": "Amarillo",
        "monitoreo": "Monitoreo cada 12 horas",
        "medidas": "Restringir actividades que generen chispas",
        "vigilancia": "Patrullaje reforzado en zonas críticas",
        "prevencion": "Comunicación a brigadas locales"
    },
    {
        "risk_category": "Riesgo alto",
        "estatus": "Alerta Naranja",
        "semaforo": "Naranja",
        "monitoreo": "Monitoreo continuo cada 2 horas",
        "medidas": "Prohibir quemas controladas. Restringir acceso a zonas forestales.",
        "vigilancia": "Vigilancia aérea y terrestre permanente",
        "prevencion": "Activación de protocolos de emergencia"
    },
    {
        "risk_category": "Riesgo muy alto",
        "estatus": "Alerta Roja",
        "semaforo": "Rojo",
        "monitoreo": "Monitoreo en tiempo real 24/7",
        "medidas": "Evacuación preventiva. Cierre total de accesos.",
        "vigilancia": "Despliegue de equipos de respuesta inmediata",
        "prevencion": "Declaratoria de emergencia. Coordinación con autoridades."
    }
]


async def init_rules():
    async with AsyncSessionLocal() as session:
        for rule_data in DEFAULT_RULES:
            stmt = select(RiskRule).where(
                RiskRule.risk_category == rule_data["risk_category"])
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            if not existing:
                rule = RiskRule(**rule_data)
                session.add(rule)
        await session.commit()
        print("Reglas inicializadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_rules())
