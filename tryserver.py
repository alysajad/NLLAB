import socket
def encrypt(text,key):
    rail=[['\n' for _ in range(len(text))]
          for _ in range (len(key))]
    dir_down=False
    row,col=0

    for ch in text:
        if row==0 or row==key-1:
            dir_down=not dir_down
        rail[row][col]=ch
        col+=1
        col+=1 if dir_down else -1
    result=""

    for i in range (key):
        for j in range(len(text)):
            if rail[i][j]!='\n':
                result+=rail[i][j]
    return result
def decrypt(text, key):
    rail=[['\n' for _ in range(len(cipher))] for _ in range (len(key))]
    dir_down=None
    row,col=0,0
    for _ in range(len(cipher)):
        if row==0:
            dir_down=True
        if row==key-1:
            dir_down=False
        rail[row][col]='*'
        col+=1
        row+=1 if dir_down else -1
    index=0
    for _ in range (len(key)):
        if rail[i][j]=='*'  and index < len(cipher):
            rail[i][j]=cipher[index]
            index+=1
    result=""
    row, col =0,0
    for _ in range(len(cipher)):
        if row==0:
            dir_down=True
        if row==key-1:
            dir_down=False
        result+=rail[row][col]
        col+=1
        row+=1 if dir_down else -1
    return result
s=socket.socket()
s.bind(('localhost',2223))
s.listen(1)
print("server lsitening")
conn, addr=s.accept()
data=conn.recv(1024).decode().split("|")
choice=data[0]
text=data[1]
if choice=='E':
    result=encrypt(text,key)
else:
    result=decrypt(text,key)

print("result at server",result)
conn.close()