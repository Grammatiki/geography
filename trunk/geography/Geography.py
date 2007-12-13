from GeographyMachine import GeographyMachine, Coords, Landmark
from WorldView import WorldView
from Timer import Timer
import time
import socket


class Geography:
    def __init__(self):
        self.geographyMachine = GeographyMachine()
        mapFile = 'images/globeSmall.gif'
        self.mapSize = (1600, 800)
        self.view = WorldView(controller=self, mapFile=mapFile, mapSize=self.mapSize)
        self.landmark = None
        self.score = 0
        self.numQuestions = 20
    
    def start(self):
        self.view.start()
        if self.timer is not None and self.timer.isAlive:
            self.timer.stop()
            time.sleep(0.2)
    
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
        if self.landmark is not None and self.timer.isAlive():
            self.numQuestions -= 1
            self.timer.stop()
            time = self.timer.time
            self.view.deleteLines()
            lat, long = self.convertCoords(event.x, event.y)
            answer = Coords(lat, long)
            distance = self.geographyMachine.checkAnswer(answer)
            # calculate score
            score = ((-5/2) * distance + 2500)  + 100 * time
            if score < 0:
                score = 0
            self.score += score
            self.view.scoreText.set("Score: %i    Total: %i" % (int(score), int(self.score)))
            self.view.answer.set("Distance: %d km" % int(distance))
            self.view.drawLines('blue', (event.x, event.y))
            x, y = self.convertCoordsBack(self.landmark.coords.lat, self.landmark.coords.long)
            self.view.drawLines('red', (x, y))
            if self.numQuestions == 0:
                self.postScore()
        
    def getQuestion(self):
        if self.numQuestions > 0:
            self.view.deleteLines()
            self.landmark = self.geographyMachine.getLandmark()
            self.view.question.set("%s, %s" % (self.landmark.name, self.landmark.country))
            self.view.answer.set("")
            self.timer = Timer(5.0, self.view.timeText)
            self.timer.start()
            
    def postScore(self):
        #self.view.scoreText.set("Final Score: %i  You must be retarded" % int(self.score))
        s = socket.socket()
        #host = socket.gethostname()
        host = "sabeto"
        port = 1234
        s.connect((host, port))
        data = "%.1f %s" % (int(self.score), self.view.nameInput.get())
        s.send(data)
        scores = "High Scores: \n"
        scores += s.recv(1024)
        print scores
        self.view.scoresText.set(scores)
 
def main():
    g = Geography()
    g.start()

if __name__ == "__main__":
    main()
        
