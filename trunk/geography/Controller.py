from Geography import GeographyMachine, Coords, Landmark
from WorldView import WorldView
import time


class Controller:
    def __init__(self):
        self.geographyMachine = GeographyMachine()
        mapFile = 'images/globeSmall.gif'
        self.mapSize = (1600, 800)
        self.view = WorldView(controller=self, mapFile=mapFile, mapSize=self.mapSize)
        self.landmark = None
    
    def start(self):
        self.view.start()
    
    def convertCoords(self, x, y):
        x = x - self.mapSize[0]/2
        y = (-1 * y) + self.mapSize[1]/2
        lat = y * 90.0 / (self.mapSize[1]/2)
        long = x * 180.0 / (self.mapSize[0]/2)
        return lat, long
    
    def convertCoordsBack(self, lat, long):
        width = self.mapSize[0]
        height = self.mapSize[1]
        x = (long * width/2) / 180
        y = (lat * height/2) / 90
        x = int(x + width/2)
        y = int(height/2 - y)
        return x, y
    
    def mouseEvent(self, event):
        if self.landmark is not None:
            self.view.deleteLines()
            lat, long = self.convertCoords(event.x, event.y)
            answer = Coords(lat, long)
            distance = self.geographyMachine.checkAnswer(answer)
            self.view.answer.set("Distance: %d km" % int(distance))
            print "lat: %f long: %f" % (lat, long)
            #self.view.canvas.create_line(0, 0, 200, 100)
            self.view.drawLines('blue', (event.x, event.y))
            #time.sleep(0.5)
            x, y = self.convertCoordsBack(self.landmark.coords.lat, self.landmark.coords.long)
            self.view.drawLines('red', (x, y))
        
    def getQuestion(self):
        self.view.deleteLines()
        self.landmark = self.geographyMachine.getLandmark()
        self.view.question.set("%s, %s" % (self.landmark.name, self.landmark.country))
        self.view.answer.set("")
        
c = Controller()
c.start()