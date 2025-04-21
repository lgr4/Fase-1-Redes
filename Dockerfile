FROM python:3.9-slim

WORKDIR /app

# Copiar arquivos
COPY server.py .
COPY client.py .
COPY client_mqtt.py .
COPY server_mqtt.py .
COPY requirements.txt .
COPY templates/ ./templates/
COPY images/ ./images/
COPY message.txt .

# Criar diretório para imagens recebidas
RUN mkdir -p images_received

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor portas
EXPOSE 5000 8082 8883

# Rodar os serviços
CMD ["sh", "-c", "python server.py & python server_mqtt.py & python client.py & python client_mqtt.py"]
