import socket 
def start_server():
    host='127.0.0.1'
    port=12345
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host,port))

    server_socket.listen(5)
    print(f"server start on {host}:{port}  waiting for connection ...")
    while True:
        client_socket,addr=server_socket.accept()
        print(f"got connection from {addr}")

        while True:
            data=client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"client says: {data}")
            message="hello client i am server  "
            client_socket.send(message.encode('utf-8'))

        client_socket.close()
        print(f"connection closed with {addr}\n")
if __name__ == "__main__":
    start_server()
