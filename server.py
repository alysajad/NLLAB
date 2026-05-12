import socket 

def start_server():
    host ='127.1.0.1'
    port=12345
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(5)
    print(f"server listening {host}:{port} wiating for connection ...")
    while True:
        data=client_socket.recv(1024).decode('utf-8')
        client_socket,addr=server_socket.accept()
        if not data:
            break
        print(f"client says {data}")
        message="hello freom server"
        server_socket.send(message.encode('utf-8'))
    client_socket.close()
    print(f"connection closed {addr}\n")
if __name__=="__main__":
    start_server()
        