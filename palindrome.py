import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    print("🔤 Connected to Palindrome Server!")
    print("   Type any string to check if it's a palindrome, or 'quit' to exit.\n")

    while True:
        text = input("Enter string: ").strip()
        if text.lower() == 'quit':
            print("Goodbye!")
            break
        if not text:
            print("Please enter a string.\n")
            continue

        client_socket.send(text.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"{response}\n")

    client_socket.close()

if __name__ == "__main__":
    client()