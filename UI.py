from tkinter import *
import socket
import threading


HOST = "127.0.0.1"
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


my_symbol = s.recv(1024).decode('utf-8')  
can_move = (my_symbol == 'X')  


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


def listen_for_moves():
    global can_move
    while True:
        try:
            data = s.recv(1024).decode('utf-8')
            if not data:
                break
            symbol, move = data.split(":")
            row, col = map(int, move.split(","))
            update_ui(symbol, row, col)

           
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


def buttonClicked(button, row, col):
    def handler():
        global can_move
        if not can_move:
            print("[BLOCKED] Not your turn.")
            return
        button.config(text=my_symbol)
        disableButton(button)
        sendMovetoServer(my_symbol, row, col)
        can_move = False
    button.config(command=handler)

#Buttons 
p1Button = Button(gameFrame, text='1', font=("Arial", 20))
p1Button.grid(row=0, column=0, sticky='nsew')
buttonClicked(p1Button, 0, 0)
button_map[(0, 0)] = p1Button

p2Button = Button(gameFrame, text='2', font=("Arial", 20))
p2Button.grid(row=0, column=1, sticky='nsew')
buttonClicked(p2Button, 0, 1)
button_map[(0, 1)] = p2Button

p3Button = Button(gameFrame, text='3', font=("Arial", 20))
p3Button.grid(row=0, column=2, sticky='nsew')
buttonClicked(p3Button, 0, 2)
button_map[(0, 2)] = p3Button

p4Button = Button(gameFrame, text='4', font=("Arial", 20))
p4Button.grid(row=1, column=0, sticky='nsew')
buttonClicked(p4Button, 1, 0)
button_map[(1, 0)] = p4Button

p5Button = Button(gameFrame, text='5', font=("Arial", 20))
p5Button.grid(row=1, column=1, sticky='nsew')
buttonClicked(p5Button, 1, 1)
button_map[(1, 1)] = p5Button

p6Button = Button(gameFrame, text='6', font=("Arial", 20))
p6Button.grid(row=1, column=2, sticky='nsew')
buttonClicked(p6Button, 1, 2)
button_map[(1, 2)] = p6Button

p7Button = Button(gameFrame, text='7', font=("Arial", 20))
p7Button.grid(row=2, column=0, sticky='nsew')
buttonClicked(p7Button, 2, 0)
button_map[(2, 0)] = p7Button

p8Button = Button(gameFrame, text='8', font=("Arial", 20))
p8Button.grid(row=2, column=1, sticky='nsew')
buttonClicked(p8Button, 2, 1)
button_map[(2, 1)] = p8Button

p9Button = Button(gameFrame, text='9', font=("Arial", 20))
p9Button.grid(row=2, column=2, sticky='nsew')
buttonClicked(p9Button, 2, 2)
button_map[(2, 2)] = p9Button


for i in range(3):
    gameFrame.rowconfigure(i, weight=1)
    gameFrame.columnconfigure(i, weight=1)


threading.Thread(target=listen_for_moves, daemon=True).start()
root.mainloop()
