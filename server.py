import socket
import os
import threading

def handle_client(client, addr):
    try:
        while True:
            data = client.recv(1024).decode()
            if not data:
                print(f"Cliente {addr} desconectado.")
                break

            if data.isdigit() and 1 <= int(data) <= 10:
                path = f"images/{data}.jpg"
                file_name = f"{data}.jpg"

                if os.path.exists(path):
                    with open(path, "rb") as file:
                        image = file.read()
                    image_size = os.path.getsize(path)

                    client.sendall(file_name.encode() + b'\n')
                    client.sendall(str(image_size).encode() + b'\n')
                    client.sendall(image)

    except Exception as e:
        print(f"Erro com cliente {addr}: {e}")
    finally:
        client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8082))
    server.listen()

    try:
        while True:
            client, addr = server.accept()
            print(f"Cliente conectado: {addr}")
            threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Servidor encerrado manualmente.")
    finally:
        server.close()

start_server()
