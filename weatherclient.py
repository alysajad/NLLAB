import socket

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    print("🌤  Connected to Weather Server!")
    print("   Type a city name to get its weather, or 'quit' to exit.\n")

    while True:
        city = input("Enter city name: ").strip()
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        if not city:
            print("Please enter a city name.\n")
            continue

        client_socket.send(city.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"{response}\n")

    client_socket.close()

if __name__ == "__main__":
    client()