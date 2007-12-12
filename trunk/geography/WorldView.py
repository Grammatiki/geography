from Tkinter import *
from PIL import Image, ImageTk

class WorldView:
    def __init__(self, controller=None, mapSize=None, mapFile=None):
        image = Image.open(mapFile)
        width, height = mapSize
        image.resize(mapSize, Image.BICUBIC)
        self.controller = controller
        self.root = Tk()
        self.topFrame = Frame(self.root)
        self.topFrame.pack(side=TOP)
        self.leftFrame = Frame(self.topFrame)
        self.leftFrame.pack(side=LEFT)
        self.rightFrame = Frame(self.topFrame)
        self.rightFrame.pack(side=RIGHT)
        #self.picture = PhotoImage(file=mapFile)
        self.question = StringVar()
        self.answer = StringVar()
        self.timeText = StringVar()
        self.scoreText = StringVar()
        self.scoresText = StringVar()
        self.nameInput = Entry(self.leftFrame)
        self.nameInput.pack()
        self.questionLabel = Label(self.leftFrame, textvariable=self.question).pack()
        self.answerLabel = Label(self.leftFrame, textvariable=self.answer).pack()
        self.scoreLabel = Label(self.leftFrame, textvariable=self.scoreText).pack()
        self.timeLabel = Label(self.leftFrame, textvariable=self.timeText).pack()
        self.button = Button(self.leftFrame, text="Get Question", command=self.controller.getQuestion)
        self.button.pack()
        self.scoresWidget = Message(self.rightFrame, textvariable=self.scoresText, width=300)
        self.scoresWidget.pack()
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
        
                  
