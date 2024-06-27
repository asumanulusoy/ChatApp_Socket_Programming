import socket
import threading

# Sunucu ayarları
HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Sunucuyla bağlantı kesildi.")
            break

# Kullanıcı adı alma
name = input("Kullanıcı adınızı girin: ")

# Sunucuya bağlanma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(bytes(name, "utf-8"))

# Sunucudan mesajları dinleme iş parçacığı başlatma
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Kullanıcıdan mesaj alıp sunucuya gönderme
while True:
    message = input()
    client_socket.send(bytes(message, "utf-8"))
