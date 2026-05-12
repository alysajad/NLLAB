import socket
c=socket.socket()
c.connect("loclahost",1234)
choice=input("enter E for encryptiona nd d for decryption").upper()
key=int(input("enter key "))
text=input("enter the text")

msg= choice + "|" + text + "|" +str(key)

c.send(msg.encode)
result=c.recv(1024).decode()

print("result is ",result)
c.close()

