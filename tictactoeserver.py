import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

clients = [None, None]  # first player gets X, second gets O
symbols = ["X", "O"]
turn = "X"  # X starts first
lock = threading.Lock()

def handle_client(conn, player_id):
    global turn
    symbol = symbols[player_id]
    other_id = 1 - player_id

    try:
        print(f"[+] Player {symbol} connected.")
        conn.sendall(symbol.encode('utf-8'))  

        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode('utf-8')
            print(f"[{symbol}] says: {msg}")

            with lock:
                if msg == "RESET":
                    print(f"[RESET] {symbol} requested a new game.")
                    turn = "X"
                    for c in clients:
                        if c:
                            c.sendall("RESET".encode('utf-8'))
                    continue  # skip rest of loop this round

                if msg.startswith(turn):  
                    if clients[other_id]:
                        try:
                            clients[other_id].sendall(data)
                        except Exception as e:
                            print(f"[!] Error relaying to {symbols[other_id]}: {e}")

                    turn = symbols[other_id]
                    print(f"[TURN] Now it's {turn}'s turn.")
                else:
                    print(f"[BLOCKED] Not {symbol}'s turn.")
    except Exception as e:
        print(f"[!] Error with player {symbol}: {e}")
    finally:
        print(f"[-] Player {symbol} disconnected.")
        clients[player_id] = None
        conn.close()

# Server loop starts
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    print("[SERVER] Waiting for 2 players...")

    while True:
        conn, addr = s.accept()

        # Assign to player X or O
        if clients[0] is None:
            player_id = 0
        elif clients[1] is None:
            player_id = 1
        else:
            conn.close()
            continue

        clients[player_id] = conn
        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()

        if all(clients):
            print("[SERVER] Both players connected. Game starting.")
