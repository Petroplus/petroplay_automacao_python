# Imagem base
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta do backend (ajuste se diferente)
EXPOSE 5000

# Comando para iniciar o backend (ajuste conforme o seu)
CMD ["python", "main.py"]
