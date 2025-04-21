from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import time

app = Flask(__name__)

broker = "localhost"
port = 1883
sending_topic = "sending"
receiving_topic = "receiving"

resposta_mqtt = None

def on_message(client, userdata, msg):
    global resposta_mqtt
    resposta_mqtt = msg.payload.decode()

@app.route("/", methods=["GET"])
def index():
    return render_template("index2.html", conteudo=None, resposta=None)

@app.route("/upload", methods=["POST"])
def upload():
    global resposta_mqtt
    resposta_mqtt = None

    arquivo = request.files["arquivo"]
    conteudo = arquivo.read().decode("utf-8")

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(receiving_topic)
    client.loop_start()

    client.publish(sending_topic, conteudo)

    timeout = 10  # segundos
    start_time = time.time()
    while resposta_mqtt is None and (time.time() - start_time) < timeout:
        time.sleep(0.1)

    client.loop_stop()
    client.disconnect()

    return render_template("index2.html", conteudo=conteudo, resposta=resposta_mqtt or "Sem resposta recebida")

if __name__ == "__main__":
    app.run(debug=True)
