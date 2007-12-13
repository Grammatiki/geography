from Tkinter import *
from PIL import Image, ImageTk
from SimpleDialog import SimpleDialog

class WorldView:
    def __init__(self, controller=None, mapSize=None, mapFile=None):
        image = Image.open(mapFile)
        width, height = mapSize
        image.resize(mapSize, Image.BICUBIC)
        self.controller = controller
        self.root = Tk()
        topFrame = Frame(self.root)
        topFrame.pack(side=TOP)
        leftFrame = Frame(topFrame)
        leftFrame.pack(side=LEFT)
        rightFrame = Frame(topFrame)
        rightFrame.pack(side=RIGHT)
        #self.picture = PhotoImage(file=mapFile)
        self.question = StringVar()
        self.answer = StringVar()
        self.timeText = StringVar()
        self.scoreText = StringVar()
        self.scoresText = StringVar()
        self.nameInput = Entry(leftFrame)
        self.nameInput.pack()
        questionLabel = Label(leftFrame, textvariable=self.question).pack()
        answerLabel = Label(leftFrame, textvariable=self.answer).pack()
        scoreLabel = Label(leftFrame, textvariable=self.scoreText).pack()
        timeLabel = Label(leftFrame, textvariable=self.timeText).pack()
        button = Button(leftFrame, text="Get Question", command=self.controller.getQuestion)
        button.pack()
        restartButton = Button(leftFrame, text="New Game", command=self.controller.restartGame)
        restartButton.pack(side=LEFT)
        scoresWidget = Message(rightFrame, textvariable=self.scoresText, width=300)
        scoresWidget.pack()
        self.picture = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.create_image(0, 0, anchor='nw', image=self.picture)
        self.canvas.bind("<Button-1>", self.controller.mouseEvent)
        self.canvas.pack(side=BOTTOM)
        self.lines = []
                
        
    def start(self):
        self.root.mainloop()
        
    def deleteLines(self):
        for i in self.lines:
            self.canvas.delete(i)
    
    def drawLines(self, color, point):
        x , y = point
        self.lines.append(self.canvas.create_line(x - 10, y - 10, x + 10, y + 10, fill=color))
        self.lines.append(self.canvas.create_line(x - 10, y + 10, x + 10, y - 10, fill=color))
        
    def showScores(self, score):
        # pop up a dialog window with some text
        SimpleDialog(self.root,
                     text=score,
                     buttons=["OK"],
                     default=0,
                     title="Demo Dialog").go()
        
                  
