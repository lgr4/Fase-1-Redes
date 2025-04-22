from flask import Flask, render_template, request,send_file, jsonify
import paho.mqtt.client as mqtt
import time
import ssl
import os
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas
app.secret_key = 'render-safe-key'  # Necessário para flash messages

broker = "1f0cc1db7e91454bb2b88eabdb55bb5f.s1.eu.hivemq.cloud"
port_broker = 8883
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

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.tls_set()
    client.on_message = on_message
    client.connect(broker, port_broker)
    client.subscribe(receiving_topic)
    client.loop_start()

    client.publish(sending_topic, conteudo)

    timeout = 10  # segundos
    start_time = time.time()
    while resposta_mqtt is None and (time.time() - start_time) < timeout:
        time.sleep(0.1)

    client.loop_stop()
    client.disconnect()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        # Requisição AJAX - Responder com JSON
        return jsonify({
            "success": True,
            "conteudo": conteudo,
            "response": resposta_mqtt or "Sem resposta recebida",
            "filename": arquivo.filename
        })
    else:
        # Requisição tradicional - Responder com HTML
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
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)
