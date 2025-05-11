from tkinter import *
from tkinter import messagebox
import socket
import threading
from game_logic import TicTacToeGame

# Setup connection
HOST = "127.0.0.1"
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Receive symbol from server
my_symbol = s.recv(1024).decode('utf-8')  
can_move = (my_symbol == 'X')  

# Game logic setup
game = TicTacToeGame()

# Tkinter setup
root = Tk()
root.title(f"Tic-Tac-Toe - You are {my_symbol}")
root.geometry("500x500")
gameFrame = Frame(root)
gameFrame.pack(fill=BOTH, expand=True)

button_map = {}

def update_ui(symbol, row, col):
    def task():
        btn = button_map.get((row, col))
        if btn:
            btn.config(text=symbol, state=DISABLED)
    root.after(0, task)

def show_game_result_popup(result):
    def ask_play_again():
        play_again = messagebox.askyesno("Game Over", f"{result}\n\nPlay again?")
        if play_again:
            try:
                s.sendall("RESET".encode('utf-8'))
            except Exception as e:
                print("[ERROR] Sending RESET:", e)
        else:
            root.destroy()
    root.after(100, ask_play_again)

def listen_for_moves():
    global can_move
    while True:
        try:
            data = s.recv(1024).decode('utf-8')
            if not data:
                break

            if data == "RESET":
                print("[INFO] Resetting game (triggered by server)")
                reset_game()
                continue

            symbol, move = data.split(":")
            row, col = map(int, move.split(","))
            update_ui(symbol, row, col)

            # Apply remote move to game logic
            game.reset_player(symbol)
            result = game.make_move(row, col)
            print("[REMOTE RESULT]", result)

            if result in ["X wins", "O wins", "Draw"]:
                print("[GAME OVER]", result)
                disable_all_buttons()
                show_game_result_popup(result)

            if symbol != my_symbol:
                can_move = True
        except Exception as e:
            print(f"[ERROR] Receiving move: {e}")
            break

def sendMovetoServer(symbol, row, col):
    try:
        move = f"{symbol}:{row},{col}"
        s.sendall(move.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Sending move: {e}")

def disableButton(button):
    button.config(state=DISABLED)

def disable_all_buttons():
    for btn in button_map.values():
        btn.config(state=DISABLED)

def reset_game():
    global game, can_move
    game.reset_game()
    can_move = (my_symbol == 'X')
    for (row, col), btn in button_map.items():
        btn.config(text=str(3 * row + col + 1), state=NORMAL)

def buttonClicked(button, row, col):
    def handler():
        global can_move
        if not can_move:
            print("[BLOCKED] Not your turn.")
            return

        # Apply local move to game logic
        game.reset_player(my_symbol)
        result = game.make_move(row, col)
        print("[LOCAL RESULT]", result)

        button.config(text=my_symbol)
        disableButton(button)
        sendMovetoServer(my_symbol, row, col)
        can_move = False

        if result in ["X wins", "O wins", "Draw"]:
            print("[GAME OVER]", result)
            disable_all_buttons()
            show_game_result_popup(result)
    button.config(command=handler)

# Button setup
for r in range(3):
    for c in range(3):
        btn = Button(gameFrame, text=str(3*r + c + 1), font=("Arial", 20))
        btn.grid(row=r, column=c, sticky='nsew')
        buttonClicked(btn, r, c)
        button_map[(r, c)] = btn

# Grid weight
for i in range(3):
    gameFrame.rowconfigure(i, weight=1)
    gameFrame.columnconfigure(i, weight=1)

# Start listening thread
threading.Thread(target=listen_for_moves, daemon=True).start()
root.mainloop()

