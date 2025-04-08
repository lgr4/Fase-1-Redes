import paho.mqtt.client as mqtt
import time

# Mensagem Original: "Hello, my name is Diego"

broker = "test.mosquitto.org"
port = 1883
sending_topic = 'sending'
receiving_topic = 'receiving'

def on_message(client, userdata, msg):
    with open(caminho, "wb") as f:
        f.write(msg.payload)
    print(f"Nova resposta salva")

client = mqtt.Client()
client.connect(broker, port, 60)

client.subscribe(receiving_topic)
client.on_message = on_message

client.loop_start()

caminho = input("Caminho do Arquivo: ")
try:
    with open(caminho, 'r') as f:
        conteudo = f.read()
        client.publish(sending_topic, conteudo)
        print(f"Conteúdo enviado:\n{conteudo}")
except FileNotFoundError:
    print("Arquivo não encontrado.")

time.sleep(15)
client.loop_stop()
client.disconnect()
