FROM python:3.9-slim

WORKDIR /app

# Copiar arquivos
COPY client_mqtt.py .
COPY server_mqtt.py .
COPY requirements.txt .
COPY templates/ ./templates/
COPY message.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor portas
EXPOSE 5001 8883

# Rodar os serviços MQTT
CMD ["sh", "-c", "python server_mqtt.py & python client_mqtt.py"]
