import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0',8082))
server.listen(2)

client,addr = server.accept()
try:    
    while True:
        data = client.recv(1024).decode()
        print(f"Mensagem recebida: {data}")
        
        if data.isdigit() and 1 <= int(data) <= 10:
            path = "images/"+data+".jpg"
            file_name = data+'.jpg'

            file = open(path,"rb")
            image = file.read()
            image_size = os.path.getsize(path)
            print(file_name)
            print(image_size)

            client.sendall(file_name.encode() + b'\n')
            client.sendall(str(image_size).encode() + b'\n')
            client.sendall(image)
            print(f"Imagem {data}.jpg enviada.")
        else:
            client.sendall("Imagem não encontrada.".encode())
            print("Imagem não encontrada.")

    #TODO Adicionar modificação de arquivos recebidos (2a parte).

except KeyboardInterrupt:

    print("Conexão Finalizada!")

except:

    print(f"Cliente {addr} desconectado.")

finally:
    client.close()
    server.close()