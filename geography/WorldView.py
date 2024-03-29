from Tkinter import *
from PIL import Image, ImageTk
from SimpleDialog import SimpleDialog
from Progress import ProgressBar
import tkSimpleDialog
from twisted.internet import tksupport
from GeographyMachine import GeographyMachine




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
    
    def __init__(self, controller=None):
        self.root = Tk()
        tksupport.install(self.root)
        #h = self.root.winfo_screenheight()
        w = self.root.winfo_screenwidth()
        self.screenSize = (w, w/2) # the width of the picture for this game is twice as wide as its height
        #d = MyDialog(self.root)
        #print "result", d.size
        self.canvas = Canvas(self.root, width=self.screenSize[0], height=self.screenSize[1])
        self.controller = controller 
        topFrame = Frame(self.root)
        topFrame.pack(side=TOP)
        self.question = StringVar()
        self.answer = StringVar()
        self.timeText = StringVar()
        self.scoreText = StringVar()
        self.scoresText = StringVar()
        self.nextRound = StringVar()
        self.nameInput = Entry(topFrame)
        self.nameInput.grid(row=0, column=1,sticky=W)
        Label(topFrame, text="Enter your name here:   ").grid(row=0, column=0, sticky=W)
        Label(topFrame, textvariable=self.question).grid(row=1, column=2, sticky=W)
        Label(topFrame, textvariable=self.answer).grid(row=1, column=3, sticky=W)
        Label(topFrame, textvariable=self.scoreText).grid(row=0, column=3, sticky=E)
        #Label(topFrame, textvariable=self.timeText).grid(row=2, column=1, sticky=W)
        self.progressBar = ProgressBar(topFrame, value=0, max=5, width=400)
        self.progressBar.grid(row=0, column=2, sticky=W)
        #self.nextRoundBar = ProgressBar(topFrame, value=5000, max=5000, width=400)
        #self.nextRoundBar.grid(row=1, column=2, sticky=W)
        Label(topFrame, textvariable=self.nextRound).grid(row=0, column=3,sticky=W)
        #Button(topFrame, text="Get Question", command=self.controller.getQuestion).grid(row=2, column=1, sticky=W)
        #Button(topFrame, text="New Game", command=self.controller.restartGame).grid(row=2, column=3, sticky=W)
        Button(topFrame, text="Quit", command=self.quit).grid(row=0, column=4, sticky=W)
        Button(topFrame, text="Restart", command=self.restart).grid(row=0, column=5, sticky=W)
        large = 1600
        self.imageId = None
        #self.makeImage(mapFile, None)
        self.canvas.bind("<Button-1>", self.controller.mouseEvent)
        self.canvas.pack(side=BOTTOM)
        self.lines = []
        self.map = None
        
        
    def makeImage(self):
        if self.imageId != None:
            print 'deleting image'
            self.canvas.delete(self.imageId)
        self.picture = ImageTk.PhotoImage(self.map.croppedImage)
        self.imageId = self.canvas.create_image(0, 0, anchor='nw', image=self.picture)
        
    def getData(self):
        self.controller.getLandmarks('easy')
        
    def restart(self):
        self.controller.restart()
        
    def start(self):
        self.root.mainloop()
        
    def quit(self):
        self.controller.quit()
        
    def deleteLines(self):
        for i in self.lines:
            self.canvas.delete(i)
            
    def startTimer(self):
        pass
    
    def updateProgressbar(self, time):
        self.progressBar.updateProgress(time)
        
    def updateNextRoundBar(self, score):
        value = self.nextRoundBar.value
        value -= score
        if value < 0:
            value = 0
        self.nextRoundBar.updateProgress(value)

    
    def drawLines(self, color, point):
        x , y = point
        self.lines.append(self.canvas.create_line(x - 10, y - 10, x + 10, y + 10, fill=color))
        self.lines.append(self.canvas.create_line(x - 10, y + 10, x + 10, y - 10, fill=color))

    def drawCircle(self, color, point, radius):
        x, y = point
        x1 = x - radius
        x2 = x + radius
        y1 = y - radius
        y2 = y + radius
        self.lines.append(self.canvas.create_oval(x1, y1, x2, y2, outline=color))
        
    def showScores(self, score):
        # pop up a dialog window with some text
        SimpleDialog(self.root,
                     text=score,
                     buttons=["OK"],
                     default=0,
                     title="Demo Dialog").go()
        
    def showMessage(self, message):
        # pop up a dialog window with some text
        SimpleDialog(self.root,
                     text=message,
                     buttons=["OK"],
                     default=0,
                     title="Demo Dialog").go()
        
    def makeLarge(self):
        pass
        

        

        



    
    
        
                  
