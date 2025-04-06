import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',8082))

def recv_line(sock):
    line = b''
    while True:
        char = sock.recv(1)
        if char == b'\n' or not char:
            break
        line += char
    return line.decode('utf-8')

try:

    while True:
        message = input()
        client.sendall(message.encode('utf-8'))
    
        file_name = recv_line(client)
        print(file_name)
        file_size = int(recv_line(client))
        print(file_size)

        image_received = b''
        while len(image_received) < file_size:
            image_part = client.recv(min(4096, file_size - len(image_received)))
            if not image_part: break
            image_received += image_part
        
        with open(file_name,'wb') as f:
            f.write(image_received)
    
    #TODO Adicionar envio de mensagem (2a parte).
    
except KeyboardInterrupt:
	client.close()