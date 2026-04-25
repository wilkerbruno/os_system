FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema para PyMySQL/cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# EasyPanel usa a variável PORT, com fallback para 5000
ENV PORT=5000

EXPOSE 5000

# Usa gunicorn em produção — workers=2 é suficiente para começar
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
