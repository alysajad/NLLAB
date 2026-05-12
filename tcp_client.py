import socket 
def client():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',12345))
    while True:
        message=input("Enter message to send to server (or 'quit' to exit): ")
        if message.lower()=='quit':
            break
        client_socket.send(message.encode('utf-8'))
        response=client_socket.recv(1024).decode('utf-8')
        print(f"Server replied: {response}\n")

    client_socket.close()
if __name__=="__main__":
    client()
