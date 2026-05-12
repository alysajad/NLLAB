import socket 
client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host="127.0.0.1"
port=1234
BUFFER_SIZE=1024
message=input("enter the message").upper()
client_socket.sendto(message.encode('utf-8'), (host, port))

data,server=client_socket.recvfrom(BUFFER_SIZE)
print(f"server says: {data.decode('utf-8')}")
client_socket.close()
