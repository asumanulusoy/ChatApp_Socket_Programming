import socket
import threading
# Sunucu ayarları
HOST = '127.0.0.1'
PORT = 55555

# Bağlı istemcilerin listesi
clients = {}
lock = threading.Lock()

# İstemciye mesaj gönderme işlevi
def broadcast(message):
    with lock:
        print(message)  # Mesajı sunucuda görüntüle
        for client_name, client_socket in clients.items():
            try:
                client_socket.send(bytes(message, "utf-8"))
            except:
                print(f"Hata: {client_name} ile bağlantı kesildi.")
                del clients[client_name]

# İstemci dinleyici işlevi
def handle_client(client_socket, client_name):
    welcome_message = f"{client_name} sohbete katıldı."
    broadcast(welcome_message)

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                broadcast(f"{client_name}: {message}")
        except:
            with lock:
                del clients[client_name]
            client_socket.close()
            broadcast(f"{client_name} sohbetten ayrıldı.")
            break

# Sunucu başlatma işlevi
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Sunucu başlatıldı. Port:", PORT)
    while True:
        client_socket, addr = server.accept()
        client_name = client_socket.recv(1024).decode("utf-8")
        clients[client_name] = client_socket
        print(f"{client_name} bağlandı. Adres: {addr}")

        # Yeni istemci iş parçacığı başlatma
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_thread.start()
        
if __name__ == "__main__":
    start_server()
