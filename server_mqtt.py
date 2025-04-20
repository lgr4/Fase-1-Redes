import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
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
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
