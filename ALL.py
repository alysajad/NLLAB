-------------TCP CLIENT-------------------------------------------------
import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))

    message = "Hello Server! This is the Client."
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server replied: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
    
    
    

    
-------------TCP SERVER-----------------------------------------------

import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1' 
    port = 12345
    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server started on {host}:{port}. Waiting for a connection...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got connection from {addr}")

        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Client says: {data}")

        message = "Hello Client! Message received."
        client_socket.send(message.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    start_server()


------------------------------------------------------------------------------------------------------------------

-------------UDP CLIENT-----------------------------------------------

import socket

SERVER_IP = "127.0.0.1"
PORT = 12345
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, Server! I am using UDP."
client_socket.sendto(message.encode('utf-8'), (SERVER_IP, PORT))

data, server = client_socket.recvfrom(BUFFER_SIZE)
print(f"Server says: {data.decode('utf-8')}")

client_socket.close()




-------------UDP SERVER-----------------------------------------------

import socket

SERVER_IP = "127.0.0.1"
PORT = 12345
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind((SERVER_IP, PORT))

print(f"UDP Server up and listening on {SERVER_IP}:{PORT}")

while True:
    data, address = server_socket.recvfrom(BUFFER_SIZE)
    
    message = data.decode('utf-8')
    print(f"Received message: '{message}' from {address}")

    response = "Message received!".encode('utf-8')
    server_socket.sendto(response, address)
    


----------------------------------------------------------------------------------------------------

-------------SINGLE CHAT CLIENT-----------------------------------------------

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12342))

    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'bye':
            break
            
        data = client_socket.recv(1024).decode('utf-8')
        if not data or data.lower() == 'bye':
            break
        print(f"Server: {data}")

    client_socket.close()

if __name__ == "__main__":
    start_client()



-------------SINGLE CHAT SERVER-----------------------------------------------

import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12342))
    server_socket.listen(1)
    
    print("Waiting for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connected to: {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data or data.lower() == 'bye':
            break
        print(f"Client: {data}")
        
        message = input("You: ")
        conn.send(message.encode('utf-8'))
        if message.lower() == 'bye':
            break

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()



----------------------------------------------------------------------------------------------------

-------------MULTI CHAT CLIENT-----------------------------------------------

import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(f"\n{data}\n -> ", end="")
        except:
            break

def send_messages(sock):
    while True:
        msg = input(" -> ")
        if msg.lower() == "bye":
            sock.send(msg.encode())
            sock.close()
            break
        sock.send(msg.encode())

def client_program():
    host = "192.168.10.101" 
    port = 5010

    sock = socket.socket()
    sock.connect((host, port))

    username = input("Enter your name: ")
    sock.send(username.encode())

    recv_thread = threading.Thread(target=receive_messages, args=(sock,))
    send_thread = threading.Thread(target=send_messages, args=(sock,))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()

if __name__ == "__main__":
    client_program()



-------------MULTI CHAT SERVER-----------------------------------------------

import socket
import threading

HOST = "0.0.0.0"
PORT = 5010

clients = {} 
lock = threading.Lock()
running = True

def broadcast(message, sender_conn=None):
    with lock:
        dead_conns = []
        for conn in clients:
            if conn != sender_conn:
                try:
                    conn.send(message.encode())
                except:
                    dead_conns.append(conn)

        for conn in dead_conns:
            conn.close()
            clients.pop(conn, None)

def handle_client(conn, addr):
    try:
        username = conn.recv(1024).decode()
        with lock:
            clients[conn] = username

        print(f"{username} joined from {addr}")
        broadcast(f"{username} joined the group")

        while True:
            msg = conn.recv(1024).decode()
            if not msg or msg.lower() == "bye":
                break

            print(f"{username}: {msg}")
            broadcast(f"{username}: {msg}", conn)

    except:
        pass
    finally:
        with lock:
            username = clients.pop(conn, "Unknown")
        broadcast(f"{username} left the group")
        conn.close()
        print(f"{username} disconnected")

def server_broadcast_input():
    global running
    while running:
        msg = input()
        broadcast(f"server: {msg}")

def server_program():
    global running
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server running...")

    threading.Thread(target=server_broadcast_input, daemon=True).start()

    while running:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()
        except:
            break

    server_socket.close()
    print("Server stopped.")

if __name__ == "__main__":
    server_program()


-----------------------------------------------------------------------------------------------------

-------------CRC CLIENT-----------------------------------------------

import socket
import time

def crc_remainder(data, gen):
    data = data + [0] * (len(gen) - 1)
    for i in range(len(data) - len(gen) + 1):
        if data[i] == 1:
            for j in range(len(gen)):
                data[i + j] ^= gen[j]
    return data[-(len(gen) - 1):]

def encode(data, gen):
    remainder = crc_remainder(data, gen)
    codeword = data + remainder
    return codeword

def client(gen, codeword):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12346))
    gen_str = ''.join(str(x) for x in gen)
    codeword_str = ''.join(str(x) for x in codeword)
    message = f"{gen_str}:{codeword_str}"
    s.send(message.encode())
    response = s.recv(1024).decode()
    print("Client received:", response)
    s.close()

if __name__ == "__main__":
    while True:
        gen_input = input("Enter the generator polynomial : ").strip()
        if len(gen_input) > 1 and all(c in '01' for c in gen_input):
            gen = [int(c) for c in gen_input]
            break
        else:
            print("Invalid generator.")
    
    while True:
        user_input = input("\nEnter binary data: ").strip().lower()
        if user_input == "exit":
            print("Exiting client.")
            break
        if not all(c in '01' for c in user_input) or len(user_input) == 0:
            print("Invalid input.")
            continue
        
        data = [int(c) for c in user_input]
        codeword = encode(data, gen)
        print(f"Encoded codeword: {codeword}")
        
        print("\nCase 1:wihtout error\n")
        client(gen, codeword)
        
        time.sleep(1)
        
        print("\nCase 2:with error\n")
        codeword_len = len(codeword)
        while True:
            error_pos = int(input(f"Enter the position to introduce the error: ").strip())
            if 1 <= error_pos <= codeword_len:
                break
            else:
                print(f"Position must be between 1 and {codeword_len}. Try again.")
        
        codeword_with_error = codeword.copy()
        codeword_with_error[error_pos - 1] = 1 - codeword_with_error[error_pos - 1]
        print(f"Codeword with error: {codeword_with_error}")
        client(gen, codeword_with_error)


-------------CRC SERVER----------------------------------------------------------------------------

import socket


def crc_remainder(data, gen):
    data = data + [0] * (len(gen) - 1)
    for i in range(len(data) - len(gen) + 1):
        if data[i] == 1:
            for j in range(len(gen)):
                data[i + j] ^= gen[j]
    return data[-(len(gen) - 1):]

def decode(codeword, gen):
    
    print(f"Received codeword: {codeword}")
    print(f"Generator polynomial: {gen} (CRC-{len(gen)-1})")
    
    remainder = crc_remainder(codeword, gen)
    print(f"remainder: {remainder}")
    
    if all(r == 0 for r in remainder):
        print("No error")
        data_len = len(codeword) - len(gen) + 1
        data = codeword[:data_len]
        return data, "No error is present"
    else:
        print("Error detected.")
        data_len = len(codeword) - len(gen) + 1
        data = codeword[:data_len]
        return data, f"Error is present (remainder: {remainder})"

def server():
    print("Server starting...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12346))
    s.listen(1)
    print("Server listening on port 12346...")
    while True:
        conn, addr = s.accept()
        print(f"\nConnection from {addr}")
        try:
            data = conn.recv(1024).decode()
            gen_str, codeword_str = data.split(':')
            gen = [int(x) for x in gen_str]
            codeword = [int(x) for x in codeword_str]
            decoded_data, status = decode(codeword, gen)
            response = f"Decoded data: {decoded_data}"
            conn.send(response.encode())
        except:
            print("Error processing client data.")
        finally:
            conn.close()
            

if __name__ == "__main__":
    server()



-----------------------------------------------------------------------------------------------------------------------------------

-------------HAMMING CLIENT-----------------------------------------------------------

import socket
import time

def calculate_parity_bits(m):
    r = 0
    while (1 << r) < m + r + 1:
        r += 1
    return r

def encode(data):
    m = len(data)
    r = calculate_parity_bits(m)
    n = m + r
    codeword = [0] * n
    j = 0
    for i in range(1, n + 1):
        if (i & (i - 1)) == 0:
            continue
        codeword[i - 1] = data[j]
        j += 1
    for i in range(r):
        parity_pos = (1 << i) - 1
        parity = 0
        for k in range(parity_pos, n, 2 * (parity_pos + 1)):
            for l in range(k, min(k + parity_pos + 1, n)):
                parity ^= codeword[l]
        codeword[parity_pos] = parity
    return codeword

def client(codeword):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12346))
    data = ''.join(str(x) for x in codeword)
    s.send(data.encode())
    response = s.recv(1024).decode()
    print("Client received:", response)
    s.close()

if __name__ == "__main__":
    while True:
        user_input = input("Enter binary data or 'exit' to quit: ").strip().lower()
        if user_input == "exit":
            print("Exiting client.")
            break
        if not all(c in '01' for c in user_input) or len(user_input) == 0:
            print("Invalid input. Please enter binary bits (0s and 1s).")
            continue
        
        data = [int(c) for c in user_input]
        codeword = encode(data)
        print(f"Encoded codeword: {codeword}")
        
        print("Test Case 1: Sending correct code")
        client(codeword)
        
        time.sleep(1)
        
        print("Test Case 2: Sending code with error")
        codeword_len = len(codeword)
        while True:
            try:
                error_pos = int(input(f"Enter the position (1-{codeword_len}) where to introduce the error: ").strip())
                if 1 <= error_pos <= codeword_len:
                    break
                else:
                    print(f"Position must be between 1 and {codeword_len}. Try again.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        
        codeword_with_error = codeword.copy()
        codeword_with_error[error_pos - 1] = 1 - codeword_with_error[error_pos - 1]
        print(f"Codeword with error: {codeword_with_error}")
        client(codeword_with_error)



-------------HAMMING SERVER----------------------------------------------------------------------------

import socket

#tyty

def calculate_parity_bits(m):
    r = 0
    while (1 << r) < m + r + 1:
        r += 1
    return r

def decode(codeword):
    print("\n--- Decoding Process ---")
    print(f"Received codeword: {codeword}")
    print("Using even parity for Hamming code.")
    
    n = len(codeword)
    r = 0
    while (1 << r) < n + 1:
        r += 1
    syndrome = 0
    for i in range(r):
        parity_pos = (1 << i) - 1
        parity = 0
        for k in range(parity_pos, n, 2 * (parity_pos + 1)):
            for l in range(k, min(k + parity_pos + 1, n)):
                parity ^= codeword[l]
        if parity != 0:
            syndrome |= (1 << i)
    print(f"Syndrome bits: s{r-1} to s0 calculated, Syndrome value: {syndrome}")
    
    if syndrome == 0:
        print("No error detected.")
        data = []
        for i in range(1, n + 1):
            if (i & (i - 1)) != 0:
                data.append(codeword[i - 1])
        return data, "No error detected"
    else:
        print(f"Error detected at position {syndrome} (1-based index).")
        pos = syndrome - 1
        print(f"Flipping bit at index {pos} in codeword.")
        codeword[pos] = 1 - codeword[pos]
        print(f"Corrected codeword: {codeword}")
        data = []
        for i in range(1, n + 1):
            if (i & (i - 1)) != 0:
                data.append(codeword[i - 1])
        print(f"Extracted corrected data: {data}")
        return data, f"Error corrected at position {syndrome}"

def server():
    print("Server starting... Using even parity for Hamming code.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12346))
    s.listen(1)
    print("Server listening on port 12346...")
    while True:
        conn, addr = s.accept()
        print(f"\nConnection from {addr}")
        try:
            data = conn.recv(1024).decode()
            codeword = [int(x) for x in data]
            decoded_data, status = decode(codeword)
            response = f"Decoded data: {decoded_data}, Status: {status}"
            conn.send(response.encode())
        except:
            print("Error processing client data.")
        finally:
            conn.close()
            print("Client disconnected.")

if __name__ == "__main__":
    server()


-----------------------------------------------------------------------------------------------------------

-------------PLAYFAIR CLIENT-----------------------------------------------

import socket

mode=input("E for Encryption, D for Decryption: ").upper()
text=input("Enter text: ")
key=input("Enter key: ")

s=socket.socket()
s.connect(("localhost",5006))
s.send(f"{mode}|{text}|{key}".encode())
result=s.recv(1024).decode()
print("Result:",result)
s.close()


-------------PLAYFAIR SERVER------------------

import socket

def generate_matrix(key):
    key=key.upper().replace("J","I")
    seen=[]
    for c in key:
        if c.isalpha() and c not in seen:
            seen.append(c)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in seen:
            seen.append(c)
    return [seen[i:i+5] for i in range(0,25,5)]

def prepare_text(text,enc=True):
    text=text.upper().replace("J","I")
    text="".join(c for c in text if c.isalpha())
    if not enc:
        return text
    res=""
    i=0
    while i<len(text):
        a=text[i]
        b=text[i+1] if i+1<len(text) else "X"
        if a==b:
            res+=a+"X"
            i+=1
        else:
            res+=a+b
            i+=2
    if len(res)%2!=0:
        res+="X"
    return res

def find(mat,c):
    for i in range(5):
        for j in range(5):
            if mat[i][j]==c:
                return i,j

def playfair(text,key,enc=True):
    mat=generate_matrix(key)
    text=prepare_text(text,enc)
    res=""
    for i in range(0,len(text),2):
        r1,c1=find(mat,text[i])
        r2,c2=find(mat,text[i+1])
        if r1==r2:
            if enc:
                res+=mat[r1][(c1+1)%5]+mat[r2][(c2+1)%5]
            else:
                res+=mat[r1][(c1-1)%5]+mat[r2][(c2-1)%5]
        elif c1==c2:
            if enc:
                res+=mat[(r1+1)%5][c1]+mat[(r2+1)%5][c2]
            else:
                res+=mat[(r1-1)%5][c1]+mat[(r2-1)%5][c2]
        else:
            res+=mat[r1][c2]+mat[r2][c1]
    return res

s=socket.socket()
s.bind(("localhost",5006))
s.listen(1)
conn,addr=s.accept()

data=conn.recv(1024).decode().split("|")
mode,text,key=data
result=playfair(text,key,mode=="E")
print("Result:",result)
conn.send(result.encode())
conn.close()



------------------------------------------------------------------------------------------------------

-------------RAILFENCE CLIENT-----------------------------------------------

import socket

c = socket.socket()
c.connect(("localhost", 9993))

choice = input("Enter E for Encryption or D for Decryption: ").upper()
text = input("Enter the text: ")
key = int(input("Enter key: "))

msg = choice + "|" + text + "|" + str(key)
c.send(msg.encode())

result = c.recv(1024).decode()
print("Result at Client:", result)

c.close()


-------------RAILFENCE SERVER-----------------------------------------------

import socket

def encrypt(text, key):
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0
    for ch in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        rail[row][col] = ch
        col += 1
        row += 1 if dir_down else -1
    result = ""
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result += rail[i][j]
    return result

def decrypt(cipher, key):
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    result = ""
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        result += rail[row][col]
        col += 1
        row += 1 if dir_down else -1
    return result

s = socket.socket()
s.bind(("localhost", 9993))
s.listen(1)
conn, addr = s.accept()

data = conn.recv(1024).decode().split("|")
choice = data[0]
text = data[1]
key = int(data[2])

if choice == "E":
    result = encrypt(text, key)
else:
    result = decrypt(text, key)

print("Result at Server:", result)
conn.send(result.encode())
conn.close()



------------------------------------------------------------------------------------------------------

-------------LZW CLIENT-----------------------------------------------

import socket
import pickle

HOST = '127.0.0.1'
PORT = 5006

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    print("\n1. Compress")
    print("2. Decompress")
    choice = input("Enter choice: ")

    if choice == "1":
        text = input("Enter the String: ")
        request = {"action": "compress", "data": text}
        client.send(pickle.dumps(request))
        compressed = pickle.loads(client.recv(4096))
        print("Output:", compressed)

    elif choice == "2":
        comp_input = input("Enter the Code : ")
        comp_list = list(map(int, comp_input.split(",")))
        request = {"action": "decompress", "data": comp_list}
        client.send(pickle.dumps(request))
        decompressed = pickle.loads(client.recv(4096))
        print("Output:", decompressed)


client.close()



-------------LZW SERVER----------------------------------------------------------------------------

import socket
import pickle

def lzw_compress(uncompressed):
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    w = ""
    result = []

    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    return result


def lzw_decompress(compressed):
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    w = chr(compressed.pop(0))
    result = w

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Bad compressed k: %s" % k)

        result += entry
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    return result



HOST = '127.0.0.1'
PORT = 5006

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server started. Waiting for connection...")

conn, addr = server.accept()
print("Connected by", addr)

while True:
    data = conn.recv(4096)
    if not data:
        break

    request = pickle.loads(data)

    if request["action"] == "compress":
        compressed = lzw_compress(request["data"])
        conn.send(pickle.dumps(compressed))

    elif request["action"] == "decompress":
        decompressed = lzw_decompress(request["data"])
        conn.send(pickle.dumps(decompressed))

conn.close()
server.close()



---------------------------------------------------------------------------------------------------------------------------

