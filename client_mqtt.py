from flask import Flask, render_template, request,send_file
import paho.mqtt.client as mqtt
import time
import ssl
from io import BytesIO

app = Flask(__name__)

broker = "1f0cc1db7e91454bb2b88eabdb55bb5f.s1.eu.hivemq.cloud"
port = 8883
username = "hivemq.webclient.1745191351074"
password = "$37:YKpE04mPtvw*n.RF"
sending_topic = 'sending'
receiving_topic = 'receiving'

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
    client.username_pw_set(username, password)
    client.tls_set()
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

@app.route("/baixar", methods=["POST"])
def baixar():
    resposta = request.form["resposta"]
    file_stream = BytesIO()
    file_stream.write(resposta.encode("utf-8"))
    file_stream.seek(0)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name="resposta.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
