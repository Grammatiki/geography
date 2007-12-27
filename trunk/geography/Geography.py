from GeographyMachine import GeographyMachine
from server.Landmark import Coords, Landmark
from WorldView import WorldView
from GameClient import GameClient
from twisted.internet import reactor, defer, task
from Timer import Timer
import time
import socket
import datetime
import random

#Last revision with twisted was 32
from server.Landmark import Landmark

class Geography:
    def __init__(self):
        self.geographyMachine = GeographyMachine()
        self.mapFile = 'images/globe.gif'
        
        #self.view = WorldView(controller=self, mapFile=mapFile, mapSize=self.mapSize)
        self.view = WorldView(controller=self, mapFile=self.mapFile)
        self.mapSize = self.view.mapSize
        self.landmark = None
        self.landmarks = None
        self.score = 0
        self.numQuestions = 20
        self.timer = None
        self.worstGuess = None
        self.client = GameClient()
        self.deferred = defer.Deferred()
        self.gameOver = False
        
        
    def start(self):
        self.getLandmarks('us')
        reactor.run()
        
    def quit(self):
        reactor.stop()
        
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
        if self.landmark is not None and self.timeLoop.running:
            self.numQuestions -= 1
            self.view.nextRound.set('%i questions left' % self.numQuestions)
            self.timeLoop.stop()
            time = self.time
            self.view.deleteLines()
            lat, long = self.convertCoords(event.x, event.y)
            answer = Coords(lat, long)
            distance = self.geographyMachine.getDistance(answer, self.landmark)
            if self.worstGuess is None:
                self.worstGuess = distance
            elif distance > self.worstGuess:
                self.worstGuess = distance
            # calculate score
            score = self.calculateScore(time, distance)
            self.score += score
            self.view.scoreText.set("Score: %i Total: %i" % (int(score),  int(self.score)))
            self.view.answer.set("Distance: %d km" % int(distance))
            self.view.drawLines('blue', (event.x, event.y))
            x, y = self.convertCoordsBack(self.landmark['lat'], self.landmark['long'])
            self.view.drawLines('red', (x, y))
            if self.numQuestions == 0:
                self.postScore()
                self.gameOver = True
        
    def getQuestion(self):
        if self.landmarks == None:
            self.landmarks = self.getLandmarks('us')
            self.getQuestion()
        elif self.numQuestions > 0:
            self.view.deleteLines()
            self.getLandmark()
            self.view.question.set("%s, %s" % (self.landmark['name'], self.landmark['country']))
            self.view.answer.set("")
            self.time = 5
            self.timeLoop = task.LoopingCall(self.updateTime)
            self.timeLoop.start(0.1)
        
    def updateTime(self):
        if self.time <= 0:
            self.timeLoop.stop()
        else:
            self.time -= 0.1
            self.view.updateProgressbar(self.time)
            
    def restart(self):
        """ """
        if self.gameOver:
            self.numQuestions = 20
            self.score = 0
            self.view.deleteLines()
            self.view.answer.set("")
            self.view.scoreText.set('')
            self.view.question.set('')
            self.getLandmarks('capitals')
            self.gameOver = False
            
    def postScore(self):
        name = self.view.nameInput.get()
        if name == '':
            name = 'anonymous'
        data = "%s %i %.1f" % (name, int(self.score), float(self.worstGuess))
        listOfScores = self.client.addScore(data)
        scores = "High Scores: \n"
        scores += listOfScores
        print scores
        self.view.scoresText.set(scores)
        self.view.showScores(scores)
        
    def getLandmarks(self, difficulty):
        print "getting landmarks"
        self.landmarks = self.client.getLandmarks(difficulty)
        return self.deferred
        
        
    def getLandmark(self):
        l = len(self.landmarks)
        if l > 0:
            d = datetime.datetime.now()
            d = d.microsecond
            random.seed(d)
            i = random.randint(0, l - 1)
            self.landmark = self.landmarks.pop(i)
            
    def calculateScore(self, time, distance):
        if distance > 2500:
            return 0.0
        score = 1000 - pow(distance, 1.2)
        timeBonus = 100 * (5 - time)
        if score < 0:
            score = 0
        score = score + timeBonus
        self.view.updateNextRoundBar(score)
        return score

        
    

                
 
def main():
    g = Geography()
    g.start()

if __name__ == "__main__":
    main()
        
