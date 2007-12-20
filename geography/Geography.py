from GeographyMachine import GeographyMachine
from server.Landmark import Coords, Landmark
from WorldView import WorldView
from GameClient import GameClient
from twisted.internet import reactor
from Timer import Timer
import time
import socket
import datetime
import random


class Geography:
    def __init__(self):
        self.geographyMachine = GeographyMachine()
        self.mapFile = 'images/globeSmall.gif'
        self.mapSize = (1600, 800)
        #self.view = WorldView(controller=self, mapFile=mapFile, mapSize=self.mapSize)
        self.view = WorldView(controller=self, mapFile=self.mapFile)
        self.landmark = None
        self.score = 0
        self.numQuestions = 2
        self.timer = None
        self.worstGuess = None
        self.getLandmarks('easy')
    
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
        if self.landmark is not None and self.view.timer.isAlive():
            self.numQuestions -= 1
            self.view.timer.stop()
            time = self.view.timer.time
            self.view.deleteLines()
            lat, long = self.convertCoords(event.x, event.y)
            answer = Coords(lat, long)
            distance = self.geographyMachine.getDistance(answer, self.landmark)
            if self.worstGuess is None:
                self.worstGuess = distance
            elif distance > self.worstGuess:
                self.worstGuess = distance
            # calculate score
            score = (-1 * distance) + 5000
            timeBonus = 100 * (5 - time)
            if score < 0:
                score = 0
            score = score + timeBonus
            self.score += score
            self.view.scoreText.set("Score: %i Total: %i" % (int(score),  int(self.score)))
            self.view.answer.set("Distance: %d km" % int(distance))
            self.view.drawLines('blue', (event.x, event.y))
            x, y = self.convertCoordsBack(self.landmark['lat'], self.landmark['long'])
            self.view.drawLines('red', (x, y))
            if self.numQuestions == 0:
                self.postScore()
        
    def getQuestion(self):
        if self.numQuestions > 0:
            self.view.deleteLines()
            self.getLandmark()
            self.view.question.set("%s, %s" % (self.landmark['name'], self.landmark['country']))
            self.view.answer.set("")
            self.view.startTimer()
            
    def restartGame(self):
        """ """
        self.geographyMachine.loadData()
        self.view.root.quit()
        self.view = WorldView(controller=self, mapFile=self.mapFile)
        self.numQuestions = 2
        self.score = 0
        self.view.deleteLines()
        self.view.answer.set("")
        self.view.scoreText.set('')
        self.view.question.set('')
        self.view.start()
            
    def postScore(self):
        data = "%s %i %.1f" % (self.view.nameInput.get(), int(self.score), float(self.worstGuess))
        client = GameClient()
        client.connect().addCallback(
            lambda _: client.addScore(data)).addCallback(
            lambda _: client.getScores()).addErrback(
            client._catchFailure).addCallback(
            lambda _: reactor.stop())
        reactor.run()
        scores = "High Scores: \n"
        scores += client.listOfScores
        print scores
        self.view.scoresText.set(scores)
        self.view.showScores(scores)
        
    def getLandmarks(self, difficulty):
        client = GameClient()
        client.connect().addCallback(
            lambda _: client.getLandmarks(difficulty)).addErrback(
            client._catchFailure).addCallback(
            lambda _: reactor.stop())
        reactor.run()
        self.landmarks = client.landmarks
        print self.landmarks
        
    def getLandmark(self):
        l = len(self.landmarks)
        if l > 0:
            d = datetime.datetime.now()
            d = d.microsecond
            random.seed(d)
            i = random.randint(0, l - 1)
            self.landmark = self.landmarks.pop(i)

        
    

                
 
def main():
    g = Geography()
    g.start()

if __name__ == "__main__":
    main()
        
