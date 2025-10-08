# -------------------------------
# Dockerfile otimizado
# -------------------------------

# Imagem base mínima e estável
FROM python:3.11-slim

# -------------------------------
# Variáveis de ambiente
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# -------------------------------
# Diretório de trabalho
# -------------------------------
WORKDIR /app

# -------------------------------
# Instala dependências do sistema
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copia requirements.txt e instala pacotes Python
# -------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Cria usuário não-root para segurança
# -------------------------------
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser appuser \
    && mkdir -p /home/appuser \
    && chown -R appuser:appuser /home/appuser

# -------------------------------
# Copia o restante do código
# -------------------------------
COPY . .

# -------------------------------
# Usa usuário não-root
# -------------------------------
USER appuser

# -------------------------------
# Porta do serviço
# -------------------------------
EXPOSE 5000

# -------------------------------
# Comando para rodar o backend
# -------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]




# # Imagem base
# FROM python:3.11-slim

# # Definir variáveis de ambiente
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONPATH=/app

# # Instalar dependências do sistema
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Define diretório de trabalho dentro do container
# WORKDIR /app

# # Copia arquivos de dependências
# COPY requirements.txt .

# # Instala dependências
# RUN pip install -r requirements.txt

# # Copia o restante do projeto
# COPY . .

# # Criar usuário não-root
# RUN useradd --create-home --shell /bin/bash appuser && \
#     chown -R appuser:appuser /app
# USER appuser


# # Expõe a porta do backend (ajuste se diferente)
# EXPOSE 8080

# # Comando para iniciar o backend (ajuste conforme o seu)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
