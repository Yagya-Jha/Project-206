import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk


screen_width = None
screen_height = None

SERVER = None
PORT  = 8080
IP_ADDRESS = '127.0.0.1'
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

ticketGrid  = []
currentNumberList = []
markedNumberList = []
flashNumberList = []
flashNumberLabel = None
gameOver = False


def showWrongMarking():
    global ticketGrid
    global flashNumberList

    for row in ticketGrid:
        for numberBox in row:
            if(numberBox['text']):
                if(int(numberBox['text']) not in flashNumberList):
                    numberBox.configure(state='disabled', background='#f48fb1',
                            foreground="white")

def markNumber(button):
    global markedNumberList

    buttonText = int(button['text'])
    markedNumberList.append(buttonText)

    button.configure(state='disabled',background='#c5e1a5', foreground="black")



def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1

        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }

        counter = 0
        while (counter < len(randomColList)):
            colNum = randomColList[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in currentNumberList):
                numberBox = ticketGrid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black")
                currentNumberList.append(randomNumber)

                counter+=1

    for row in ticketGrid:
        for numberBox in row:
            if(not numberBox['text']):
                numberBox.configure(state='disabled', background='#ff8a65')


def createTicket():
    global gameWindow
    global ticketGrid

    mianLable = Label(gameWindow, width=75, height=16,relief='ridge', borderwidth=5, bg='white')
    mianLable.place(x=screen_width/2-130, y=screen_height/2-100)

    xPos = screen_width/2-200
    yPos = screen_height/2-150
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            boxButton = Button(gameWindow, font = ("Chalkboard SE",30), width=3, height=2,borderwidth=5, bg="#fff176")
            boxButton.configure(command = lambda boxButton=boxButton : markNumber(boxButton))
            boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64

        ticketGrid.append(rowList)
        xPos = screen_width/2-200
        yPos +=82



def gamewindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Game")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = screen_width,height = screen_height)
    canvas2.pack(fill = "both", expand = True)

    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    canvas2.create_text( screen_width/2,screen_height-200, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="red")

    createTicket()
    placeNumbers()


    flashNumberLabel = canvas2.create_text(screen_width/2,200, text = "Waiting for other players to join...", font=("Chalkboard SE",30), fill="#3e2723")

    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gamewindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2,screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="#3e2723")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/2-180, y=screen_height/2-10 )

    button = Button(nameWindow, text="Join", font=("Chalkboard SE", 30),width=11, command=saveName, height=2, bg="red", bd=3)
    button.place(x = screen_width/2 - 150, y=screen_height/2 + 100)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def recivedMsg():
    pass


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()

setup()