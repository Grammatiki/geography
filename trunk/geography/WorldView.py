from Tkinter import *
from PIL import Image, ImageTk
from SimpleDialog import SimpleDialog
from Progress import ProgressBar
import tkSimpleDialog
from Timer import Timer

class MyDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="Size:").grid(row=0)
        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1 # initial focus

    def apply(self):
        self.size = int(self.e1.get())
        print self.size  # or something

class WorldView:
    
    def __init__(self, controller=None, mapFile=None):
        self.root = Tk()
        #d = MyDialog(self.root)
        #print "result", d.size
        self.mapSize = (1600, 800)
        image = Image.open(mapFile)
        width, height = self.mapSize
        image.resize(self.mapSize, Image.BICUBIC)
        self.controller = controller   
        topFrame = Frame(self.root)
        topFrame.pack(side=TOP)
        self.question = StringVar()
        self.answer = StringVar()
        self.timeText = StringVar()
        self.scoreText = StringVar()
        self.scoresText = StringVar()
        self.nameInput = Entry(topFrame)
        self.nameInput.grid(row=0, column=1,sticky=W)
        Label(topFrame, text="Enter your name here:   ").grid(row=0, column=0, sticky=W)
        Label(topFrame, textvariable=self.question).grid(row=2, column=0, sticky=W)
        Label(topFrame, textvariable=self.answer).grid(row=1, column=1, sticky=W)
        Label(topFrame, textvariable=self.scoreText).grid(row=1, column=0, sticky=W)
        #Label(topFrame, textvariable=self.timeText).grid(row=2, column=1, sticky=W)
        self.progressBar = ProgressBar(topFrame, value=0, max=5, width=400)
        self.progressBar.grid(row=2, column=2, sticky=W)
        Button(topFrame, text="Get Question", command=self.controller.getQuestion).grid(row=2, column=1, sticky=W)
        Button(topFrame, text="New Game", command=self.controller.restartGame).grid(row=2, column=3, sticky=W)
        large = 1600
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
            
    def startTimer(self):
        self.timer = Timer(5.0, self.updateProgressbar)
        self.timer.start()
    
    def updateProgressbar(self, time):
        self.progressBar.updateProgress(time)

    
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
        
    def makeLarge(self):
        pass
        

        

        



    
    
        
                  
