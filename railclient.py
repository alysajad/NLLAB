import socket
c=socket.socket()
c.connect(("localhost",9933))
choice=input("enter the E for encryption adn D for decryption ").upper()
text=input("enter the text")
key=int(input("enter the key "))

msg= choice +"|"+text+"|" + str(key)
c.send(msg.encode())

result=c.recv(1024).decode()
print("result is ",result)

c.close()
