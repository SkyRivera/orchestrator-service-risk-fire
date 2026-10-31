CREATE TABLE IF NOT EXISTS risk_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    risk_category VARCHAR(50) NOT NULL UNIQUE,
    estatus VARCHAR(100) NOT NULL,
    semaforo VARCHAR(50) NOT NULL,
    monitoreo VARCHAR(200) NOT NULL,
    medidas VARCHAR(500) NOT NULL,
    vigilancia VARCHAR(200) NOT NULL,
    prevencion VARCHAR(500) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    priority INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS audit_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    correlation_id UUID,
    device_id VARCHAR(64) NOT NULL,
    input_data JSONB NOT NULL,
    nubosity_response JSONB,
    vegetation_response JSONB,
    telemetry_response JSONB,
    risk_fire_response JSONB,
    rule_evaluation JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'success',
    error_message VARCHAR(500),
    processing_time_ms DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

INSERT INTO risk_rules (risk_category, estatus, semaforo, monitoreo, medidas, vigilancia, prevencion) VALUES
('Riesgo bajo', 'Normal', 'Verde', 'Monitoreo rutinario cada 24 horas', 'Sin restricciones.', 'Patrullaje estándar', 'Mantenimiento preventivo'),
('Riesgo medio', 'Alerta Amarilla', 'Amarillo', 'Monitoreo cada 12 horas', 'Restringir actividades con chispas', 'Patrullaje reforzado', 'Comunicación a brigadas'),
('Riesgo alto', 'Alerta Naranja', 'Naranja', 'Monitoreo cada 2 horas', 'Prohibir quemas', 'Vigilancia permanente', 'Protocolos de emergencia'),
('Riesgo muy alto', 'Alerta Roja', 'Rojo', 'Monitoreo 24/7', 'Evacuación preventiva', 'Equipos de respuesta', 'Declaratoria de emergencia')
ON CONFLICT (risk_category) DO NOTHING;