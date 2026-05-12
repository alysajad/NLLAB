import socket

def start_client():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host='127.0.0.1'
    port=12345
    client_socket.connect('host',port)
    while True:
        message=input("enter the message")
        if message.lower()=='quit':
            break
        client_socket.send(message.encode('utf-8'))
        response=client_socket.recv(1024).decode('utf-8')
        print(f"server replied {response}\n")
    client_socket.close()
if __name__=="__main__":
    start_client()
    