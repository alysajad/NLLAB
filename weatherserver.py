import socket

# Dummy weather data: city -> (temperature, state/condition)
CITY_WEATHER = {
    "mumbai":     ("32°C", "Humid & Partly Cloudy"),
    "delhi":      ("41°C", "Hot & Sunny"),
    "bangalore":  ("24°C", "Pleasant & Clear"),
    "chennai":    ("35°C", "Hot & Humid"),
    "kolkata":    ("33°C", "Cloudy with Light Rain"),
    "hyderabad":  ("29°C", "Partly Cloudy"),
    "pune":       ("27°C", "Breezy & Clear"),
    "jaipur":     ("38°C", "Dry & Sunny"),
    "ahmedabad":  ("36°C", "Hot & Dry"),
    "surat":      ("31°C", "Humid & Overcast"),
    "london":     ("14°C", "Foggy & Drizzly"),
    "new york":   ("22°C", "Sunny & Windy"),
    "tokyo":      ("18°C", "Mild & Clear"),
    "paris":      ("16°C", "Cloudy & Cool"),
    "dubai":      ("44°C", "Scorching & Sunny"),
}

def get_weather(city_name):
    city = city_name.strip().lower()
    if city in CITY_WEATHER:
        temp, state = CITY_WEATHER[city]
        return f"🌡  {city_name.title()} → Temperature: {temp} | Condition: {state}"
    else:
        return f"⚠  Sorry, no weather data found for '{city_name}'. Try: {', '.join(c.title() for c in CITY_WEATHER)}"

def start_server():
    host = '127.0.0.1'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SERVER] Weather server started on {host}:{port} — waiting for connections...")
    print(f"[SERVER] Available cities: {', '.join(c.title() for c in CITY_WEATHER)}\n")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Connection from {addr}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            city_name = data.strip()
            print(f"[SERVER] Client asked about: '{city_name}'")
            response = get_weather(city_name)
            client_socket.send(response.encode('utf-8'))

        client_socket.close()
        print(f"[SERVER] Connection closed with {addr}\n")

if __name__ == "__main__":
    start_server()