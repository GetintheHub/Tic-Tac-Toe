import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

clients = []
addresses = []

# Accept and store two clients
def accept_clients(server_socket):
    while len(clients) < 2:
        conn, addr = server_socket.accept()
        clients.append(conn)
        addresses.append(addr)
        print(f"Player {len(clients)-1} connected from {addr}")

        # Send START,<player_id> to the client
        conn.sendall(f"START,{len(clients)-1}".encode())

    print("Both players connected. Game can begin.")

# Start the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")

    accept_clients(s)

    # Main loop for receiving and broadcasting moves
    while True:
        for idx, conn in enumerate(clients):
            try:
                conn.settimeout(0.1)
                data = conn.recv(1024).decode()
                if data:
                    print(f"Player {idx} sent: {data}")
                    # Broadcast to both players
                    for client in clients:
                        client.sendall(data.encode())
            except socket.timeout:
                continue
            except ConnectionResetError:
                print(f"Player {idx} disconnected.")
                conn.close()
                clients.remove(conn)
