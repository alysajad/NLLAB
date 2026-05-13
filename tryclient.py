import socket
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def client():
    host='127.0.0.1'
    port=1234
    client_socket.connect((host,port))
    print(f" connected to the {host}:{port}")

    while True:
        message=input("enter the message : \n ")
        print("server recieved : ",message)
        if message.lower()=='quit':
            break
        client_socket.send(message.encode('utf-8'))
        response=client_socket.recv(1024).decode('utf-8')
        print(f"server responded with : {response} ")
    client_socket.close()

if __name__=="__main__":
    client()
    


