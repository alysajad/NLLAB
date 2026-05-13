import socket
def generate_hamming(data):
    d1,d2,d3,d4,d5,d6,d7,d8=map(int,data)
    p1=d1^d2^d4^d5^d7
    p2=d1^d3^d4^d6^d7
    p3=d2^d3^d4^d8
    p4=d5^d6^d7^d8
    return [p1, p2, d1, d2, p3, d3, d4, p4, d5, d6, d7, d8]
def introduce_error(code,pos):
    code[pos-1]^=1
    return code
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
s = socket.socket()
s.connect(('localhost', 12345))

data = input("enter 8 bit data\n")
code = generate_hamming(data)              # define code FIRST
print("generated hamming code", code)

pos = int(input("enter the pos for error, 0 for no error"))  # define pos FIRST
if pos != 0:
    code = introduce_error(code, pos)      # use AFTER both exist

print("data after error", code)
print("sending hamming code to server")
s.send("".join(map(str, code)).encode())
ack = s.recv(1024).decode()
print(ack)
s.close()