import socket
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server():

    host='127.0.0.1'
    port=1234
    server_socket.bind((host,port))

    server_socket.listen(5)
    while True:
        client_socket, addr=server_socket.accept()

        print(f" connected with {addr}")

        while True:
            data=client_socket.recv(1024).decode()
            if not data or data.lower()=='bye':
                break
            print(f"server said", data)

            message=input("enter server message : \n ")
            print("YOU :", message)
            client_socket.send(message.encode('utf-8'))

            if message.lower()=='bye':
                break

        client_socket.close()
if __name__=="__main__":
    server()


    
