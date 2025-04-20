import paho.mqtt.client as mqtt
import time
import ssl

'''
Usar se for utilizar o broker público

broker = "1f0cc1db7e91454bb2b88eabdb55bb5f.s1.eu.hivemq.cloud"
port = 8883
username = "hivemq.webclient.1745191351074"
password = "$37:YKpE04mPtvw*n.RF"
sending_topic = 'sending'
receiving_topic = 'receiving'
'''

broker = "localhost"
port = 1883
sending_topic = 'sending'
receiving_topic = 'receiving'

def on_message(client, userdata, msg):
    with open(caminho, "wb") as f:
        f.write(msg.payload)
    print(f"Nova resposta salva")

client = mqtt.Client()

'''
Usar se for utilizar o broker público

client.username_pw_set(username, password)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
'''

client.connect(broker, port)
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
