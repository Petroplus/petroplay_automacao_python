# Imagem base
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências
RUN pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser


# Expõe a porta do backend (ajuste se diferente)
EXPOSE 5000

# Comando para iniciar o backend (ajuste conforme o seu)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
