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
        
        self.timer = None
        self.worstGuess = None
        self.client = GameClient()
        self.deferred = defer.Deferred()
        self.setRounds()
        
    def setRounds(self):
        self.gameOver = False
        self.rounds = ['world', 'us']
        self.roundNumber = 0
        
        
    def start(self):
        self.nextRound()
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
        if self.landmark is not None:
            if len(self.landmarks) == 0 or not self.timeLoop.running:
                self.nextRound("Sorry, you didn't guess in time")
            elif self.timeLoop.running:
                lat, long = self.convertCoords(event.x, event.y)
                answer = Coords(lat, long)
                self.timeLoop.stop()
                distance = self.geographyMachine.getDistance(answer, self.landmark)
                self.view.drawLines('blue', (event.x, event.y))
                x, y = self.convertCoordsBack(self.landmark['lat'], self.landmark['long'])
                self.view.drawLines('red', (x, y))
                self.view.answer.set("Distance: %d km" % int(distance))
                if distance > 500:
                    self.nextRound("Sorry, you missed by more than 500 km")
                else:
                    self.view.nextRound.set('%i questions left' % len(self.landmarks))       
                    time = self.time
                    self.view.deleteLines()
                    if self.worstGuess is None:
                        self.worstGuess = distance
                    elif distance > self.worstGuess:
                        self.worstGuess = distance
                    # calculate score
                    score = self.calculateScore(time, distance)
                    self.score += score
                    self.view.scoreText.set("Score: %i Total: %i" % (int(score),  int(self.score)))
                    
                    
            
                
    def nextRound(self, message):
        if len(self.rounds) > 0:
            round = self.rounds.pop()
            self.roundNumber += 1
            if self.landmarks == None:
                message = "Choose the position of the given city.  If you miss by more than 500 km, the round is over"
            message = message + "\n\nRound %i: The 50 most populus cities of the %s" % (self.roundNumber, round)
            self.view.showRound(message)
            self.getLandmarks(round)
        else:
            self.gameOver = True
            self.view.showRound("Game over, now attempting to post your score to the server")
            self.postScore()
        
    def getQuestion(self):
        if self.landmarks == None:
            pass
            #self.landmarks = self.getLandmarks('world')
            #self.getQuestion()
        elif len(self.landmarks) > 0:
            self.view.deleteLines()
            self.getLandmark()
            self.view.question.set("%s, %s" % (self.landmark['name'], self.landmark['country']))
            self.view.answer.set("")
            self.time = 5
            self.timeLoop = task.LoopingCall(self.updateTime)
            self.timeLoop.start(0.1)
        else:
            self.nextRound("Good job, you got all 50!")
        
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
            self.getLandmarks('europeTopTwenty')
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
        self.landmark = self.landmarks.pop()
            
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
        
