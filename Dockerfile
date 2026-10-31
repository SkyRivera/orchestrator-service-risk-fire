# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.12.1-slim AS builder

WORKDIR /build

# Instalar dependencias del sistema para compilar paquetes (asyncpg, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear entorno virtual e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Runtime
# ==========================================
FROM python:3.12.1-slim AS runtime

WORKDIR /app

# Instalar dependencias mínimas del sistema en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el entorno virtual desde el builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar el código de la aplicación
COPY ./app /app/app

# Crear usuario no root para mayor seguridad
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]