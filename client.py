import socket
import threading
import os
from flask import Flask, render_template,request,send_from_directory

app = Flask(__name__, static_folder='images')
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg and msg.isdigit() and 1 <= int(msg) <= 10:
            socket_receiver(message=msg)
    return render_template('index.html', image=received_images[-1] if received_images else None)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images_received', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
