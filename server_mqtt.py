import paho.mqtt.client as mqtt
import ssl

broker = "1f0cc1db7e91454bb2b88eabdb55bb5f.s1.eu.hivemq.cloud"
port = 8883
username = "hivemq.webclient.1745191351074"
password = "$37:YKpE04mPtvw*n.RF"
sending_topic = 'sending'
receiving_topic = 'receiving'

def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado: " + str(rc))
    client.subscribe(sending_topic) 
def on_message(client, userdata, msg):
    mensagem_recebida = msg.payload.decode()
    print(f"Mensagem recebida no tópico {msg.topic}: {mensagem_recebida}")
    nome = mensagem_recebida.split()[-1]  
    nova_mensagem = f"A pleasure, {nome}"
    client.publish(receiving_topic, nova_mensagem)

client = mqtt.Client()

client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_forever()
