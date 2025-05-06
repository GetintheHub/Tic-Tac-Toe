from tkinter import *

# Function for starting the game 
def gameStartedUI(start):
    if start == 1:
        root = Tk()
        root.title("Tic-Tac-Toe")
        root.geometry("500x500")

        gameFrame = Frame(root)
        gameFrame.pack(fill=BOTH, expand=True)

        # Creates grid
        for i in range(3):
            gameFrame.rowconfigure(i, weight=1)
            gameFrame.columnconfigure(i, weight=1)


        #Button functionality 
        def changeCharacter(b):
            b.config(text = 'X')
       
                
                
        
            

        def buttonClicked(button):
            button.configure(command = lambda b = button: changeCharacter(b))
            

            

        
            
        p1Button = Button(gameFrame, text='1')
        p1Button.grid(row=0, column=0, sticky='nsew')
        buttonClicked(p1Button)

        p2Button = Button(gameFrame, text='2')
        p2Button.grid(row=0, column=1, sticky='nsew')
        buttonClicked(p2Button)

        p3Button = Button(gameFrame, text='3')
        p3Button.grid(row=0, column=2, sticky='nsew')
        buttonClicked(p3Button)

        p4Button = Button(gameFrame, text='4')
        p4Button.grid(row=1, column=0, sticky='nsew')
        buttonClicked(p4Button)

        p5Button = Button(gameFrame, text='5')
        p5Button.grid(row=1, column=1, sticky='nsew')
        buttonClicked(p5Button)

        p6Button = Button(gameFrame, text='6')
        p6Button.grid(row=1, column=2, sticky='nsew')
        buttonClicked(p6Button)

        p7Button = Button(gameFrame, text='7')
        p7Button.grid(row=2, column=0, sticky='nsew')
        buttonClicked(p7Button)

        p8Button = Button(gameFrame, text='8')
        p8Button.grid(row=2, column=1, sticky='nsew')
        buttonClicked(p8Button)

        p9Button = Button(gameFrame, text='9')
        p9Button.grid(row=2, column=2, sticky='nsew')
        buttonClicked(p9Button)

        root.mainloop()

start = 1
gameStartedUI(start)