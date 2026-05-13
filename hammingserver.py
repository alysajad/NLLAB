import socket
def detect_and_correct(code):
    p1=code[0]^code[2]^code[4]^code[6]^code[8]^code[10]
    p2=code[1]^code[2]^code[5]^code[6]^code[9]^code[10]
    p3=code[3]^code[4]^code[5]^code[6]^code[11]
    p4=code[7]^code[8]^code[9]^code[10]^code[11]
    error_pos=p4*8+p3*4+p2*2+p1

    if error_pos!=0:
        print(f"error detected at :",error_pos)
        code[error_pos-1]^=1
        print(f"error corrected.Corrected_code:",code)
    else:
        print("no error detected")

    return code

s=socket.socket()
s.bind(('localhost',12345))
s.listen(1)
print("server is waiting for connection ...")
conn,addr=s.accept()
print("connected to client", addr)

raw=conn.recv(1024).decode()

code = [int(c) for c in raw]
print("recieved from client",code)
corrected=detect_and_correct(code)
conn.send("server: code recieved and the correction done ".encode())
conn.close()
