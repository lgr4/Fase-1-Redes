import socket
import threading
import os
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for

app = Flask(__name__, static_folder='images')
app.secret_key = 'render-safe-key'  # Necessário para flash messages
os.makedirs('images', exist_ok=True)
os.makedirs('images_received', exist_ok=True)

received_images = []

def recv_line(sock):
    line = b''
    while True:
        char = sock.recv(1)
        if char == b'\n' or not char:
            break
        line += char
    return line.decode('utf-8')

def socket_receiver(message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 8082))
        client.sendall(message.encode('utf-8'))

        file_name = recv_line(client)
        file_size = int(recv_line(client))
        image_received = b''
        while len(image_received) < file_size:
            image_part = client.recv(min(4096, file_size - len(image_received)))
            if not image_part: break
            image_received += image_part

        unique_name = f"{file_name}"
        path = os.path.join('images_received', unique_name)
        with open(path, 'wb') as f:
            f.write(image_received)
        received_images.append(unique_name)
        return True, None
    except Exception as e:
        print(f"Erro ao conectar ao servidor TCP: {e}")
        return False, str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_msg = None
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg and msg.isdigit() and 1 <= int(msg) <= 10:
            ok, err = socket_receiver(message=msg)
            if not ok:
                error_msg = f"Não foi possível conectar ao servidor TCP. Funcionalidade limitada no ambiente Render. Erro: {err}"
                flash(error_msg, 'danger')
    image = received_images[-1] if received_images else None
    return render_template('index.html', image=image)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images_received', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
