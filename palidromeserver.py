import socket

def is_palindrome(text):
    # Manually clean: keep only alphanumeric, lowercase
    cleaned = ""
    for c in text:
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9'):
            cleaned += c.lower()

    # Manually check palindrome using two pointers
    left = 0
    right = len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True

def start_server():
    host = '127.0.0.1'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SERVER] Palindrome server started on {host}:{port} — waiting for connections...\n")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Connection from {addr}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"[SERVER] Received: '{data}'")
            if is_palindrome(data):
                response = f"✅ '{data}' IS a palindrome!"
            else:
                response = f"❌ '{data}' is NOT a palindrome."
            client_socket.send(response.encode('utf-8'))

        client_socket.close()
        print(f"[SERVER] Connection closed with {addr}\n")

if __name__ == "__main__":
    start_server()