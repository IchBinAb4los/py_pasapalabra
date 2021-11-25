import threading
import time
from tkinter import *

SHADOW_DEFAULT_LETTER = ("Helvetica", "23", "bold")
DEFAULT_LETTER = ("Helvetica", "20", "bold")
DEFAULT_QUESTION = ("Helvetica", "10", "bold")
DEFAULT_TIME = ("Helvetica", "28", "bold")
TIME = 230

x, y, s = 500, 500, 5
circlesPos = {}

questions = {"A":["Planta con raíz comestible, de color blanco y olor fuerte.", "ajo"],
             "B":["Palo de madera que sirve para apoyarse al andar.", "baston"],
             "C":["Planta verde con muchas espinas.", "cactus"],
             "D":["Estructura anatómica calcificada que se localiza en la cavidad oral.", "diente"],
             "E":["Sujetar, unir o colgar una cosa con un gancho u otra cosa parecida.", "enganchar"],
             "F":["Personas o cosas colocadas en línea, una detrás de otra.", "fila"],
             "G":["Gesto de cerrar un solo ojo durante un momento.", "guiñar"],
             "H":["Pieza de metal que sirve para adornar o cerrar bolsos, cinturones...", "hebilla"],
             "I":["Gran trozo de hielo que flota en el mar.", "iceberg"],
             "J":["Sustancia que sirve para lavar.", "jabon"],
             "K":["Salsa agridulce de origen chino hecha de tomates.", "ketchup"],
             "L":["Cinta anudada que sirve para atar y adornar.", "lazo"],
             "M":["Pieza de tela con la que se cubre la mesa durante las comidas.", "mantel"],
             "N":["Ninguna persona.", "nadie"],
             "Ñ":["Tipo de pasta italiana elaborada con papa. (singular)", "ñoqui"],
             "O":["Percibir sonidos a través del oído.", "oir"],
             "P":["Dar dinero a una persona a cambio de un objeto/servicio.", "pagar"],
             "Q":["Convertir en trozos algo que es duro.", "quebrar"],
             "R":["Sonido que produce el caballo.", "relincho"],
             "S":["Cortar la hierba u otras plantas.", "segar"],
             "T":["Bicicleta para dos o más personas.", "tandem"],
             "U":["Contrario de 'primero'.", "ultimo"],
             "V":["Planta cuyo fruto es la uva.", "vid"],
             "W":["Jugador de waterpolo.", "waterpolista"],
             "X":["Parte blanda ubicada al final del esternón humano.", "xifoides"]
             }

letters = [["A", "B", "C", "D", "E"],
           ["F", "G", "H", "I", "J"],
           ["K", "L", "M", "N", "Ñ"],
           ["O", "P", "Q", "R", "S"],
           ["T", "U", "V", "W", "X"]]

_letters = []

for i in letters:
    _letters.extend(i)

startPos = [145-s, 130-s, 145+30+s, 130+30+s]
x1, y1, x2, y2 = startPos
_x = 44
_y = 45

for l in letters:
    for i in range(len(l)):
        circlesPos[l[i]] = [x1, y1, x2, y2]
        x1 += _x; x2 += _x
    startPos = [startPos[0], startPos[1]+45, startPos[2], startPos[3]+45]
    x1, y1, x2, y2 = startPos

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Pasapalabra")
        self.root.geometry(str(x)+"x"+str(y))
        self.root.iconbitmap("img/icon.ico")
        self.root.resizable(False, False)
        self.c = Canvas(self.root, width=x, height=y, bg="#dedede")
        self.c.pack()
        self.circles = self.createCircles()
        self.fQuestion = self.createfQuestion()
        self.fStart = self.createfStart()
        self.fAns = self.createfAns()
        self.fPP = self.createfPP()
        self.timeLeft = TIME
        self.fTime = self.createfTime()
        self.currentLetter = "A"
        self.currentLetterIndex = 0
        self.right = 0
        self.wrong = 0
        self.playing = False
        self.firstTime = True
        self.root.bind("<Key>", self.pressKey)

    def pressKey(self, event):
        if event.keysym == "Return":
            self.fStart.invoke()

    def updateQuestion(self, l, q, a):
        self.c.itemconfig(self.fQuestion, text=q)
        for k,v in self.circles.items():
            if k == l:
                self.c.itemconfig(self.circles[l], fill="#25b8d9")

    def finish(self):
        self.c.itemconfig(self.fQuestion, text=f"¡Tuviste {self.right} aciertos y {self.wrong} errores!")
        self.fStart.config(command=self.startGame)
        self.fPP.config(command=NONE)
        self.playing = False

    def PP(self):
        for k, v in self.circles.items():
            if k == self.currentLetter:
                self.c.itemconfig(self.circles[self.currentLetter], fill="#b3bf06")
        if not self.currentLetter == "X":
            self.currentLetter = _letters[self.currentLetterIndex + 1]
            self.updateQuestion(self.currentLetter, questions[self.currentLetter][0], questions[self.currentLetter][1])
            self.currentLetterIndex += 1
        else:
            self.finish()
        self.fAns.delete(0, END)

    def nextQ(self):
        _try = self.fAns.get().lower()
        ans = questions[self.currentLetter][1]
        color = ""
        if _try == ans:
            color = "#1fbf06"
        else:
            color = "#bf0606"
        if color == "#1fbf06":
            self.right += 1
        else:
            self.wrong += 1
        for k, v in self.circles.items():
            if k == self.currentLetter:
                self.c.itemconfig(self.circles[self.currentLetter], fill=color)
        if not self.currentLetter == "X":
            self.currentLetter = _letters[self.currentLetterIndex + 1]
            self.updateQuestion(self.currentLetter, questions[self.currentLetter][0], questions[self.currentLetter][1])
            self.currentLetterIndex += 1
        else:
            self.finish()
        self.fAns.delete(0, END)

    def updateTime(self):
        if self.playing:
            try:
                time.sleep(1)
                self.timeLeft -= 1
                self.c.itemconfig(self.fTime, text=str(self.timeLeft))
                if not self.c.itemcget(self.fTime, "text") == "0":
                    self.updateTime()
                else:
                    time.sleep(1)
                    self.finish()
            except RuntimeError:
                pass

    def startGame(self):
        self.fAns.delete(0, END)
        del(self.circles)
        self.circles = self.createCircles()
        self.playing = True
        self.timeLeft = TIME
        self.currentLetter = "A"
        self.currentLetterIndex = 0
        self.right = 0
        self.wrong = 0
        self.c.itemconfig(self.fQuestion, text="")
        if self.firstTime:
            threading.Thread(target=self.updateTime).start()
        self.updateQuestion(self.currentLetter, questions[self.currentLetter][0], questions[self.currentLetter][1])
        self.fStart.config(command=self.nextQ)
        self.fPP.config(command=self.PP)

    def createfPP(self):
        b = Button(self.root, text="Pasapalabra", bd=4, width=10, font=("Helvetica", "15", "bold"))
        b.place(x=180, y=422)
        return b

    def createfAns(self):
        l = Entry(self.root, width=42, bd=3)
        l.place(x=120, y=500-115)
        return l

    def createfStart(self):
        b = Button(self.root, command=self.startGame, text=u"\u25b6", bd=4, width=4, font=("Helvetica", "20", "bold"))
        b.place(x=x-100, y=416)
        return b

    def createfTime(self):
        c = self.c.create_oval(20, 410, 90, 480, fill="#e6e6e6", width=2)
        t = self.c.create_text(eval("(20+90)//2"), eval("(410+480)//2"), text=str(self.timeLeft),
                               font=DEFAULT_TIME)
        return t

    def createfQuestion(self):
        l = self.c.create_rectangle(30, 30, x-30, 70, fill="#e6e6e6", width=2)
        t = self.c.create_text(eval("(30+x-30)//2"), eval("(30+70)//2"), text="", font=DEFAULT_QUESTION)
        return t

    def createCircles(self):
        _dict = {}
        for k,v in circlesPos.items():
            x1, y1, x2, y2 = v
            c = self.c.create_oval(x1, y1, x2, y2, fill="#1d53ab", width=1.5)
            _t = self.c.create_text(eval("(x1+x2)//2"), eval("(y1+y2)//2"), text=k, fill="#000000", font=SHADOW_DEFAULT_LETTER)
            t = self.c.create_text(eval("(x1+x2)//2"), eval("(y1+y2)//2"), text=k, fill="#ffffff", font=DEFAULT_LETTER)
            _dict[self.c.itemcget(t, "text")] = c
        return _dict

    def loop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.loop()
