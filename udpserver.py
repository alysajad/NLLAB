import socket
host="127.0.0.1"
port=1234
BUFFER_SIZE=1024
server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind((host,port))
while True:
    data,addr=server_socket.recvfrom(BUFFER_SIZE)
    message=data.decode('utf-8')
    print(f"message {message} from {addr}")
    response=message.encode('utf-8')
    server_socket.sendto(response,addr)
    