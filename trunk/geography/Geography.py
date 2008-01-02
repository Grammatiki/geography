from Map import Map
from server.Landmark import Coords, Landmark
from WorldView import WorldView
from GameClient import GameClient, ConnectionError
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
        mapFile = 'images/world.tif'
        #self.view = WorldView(controller=self, mapFile=mapFile, mapSize=self.mapSize)
        self.view = WorldView(controller=self)
        self.map = Map(mapFile, screenSize=self.view.screenSize)
        self.view.map = self.map
        self.landmark = None
        self.landmarks = None
        self.score = 0
        self.maximumDistance = 1000
        self.timer = None
        self.worstGuess = None
        self.client = GameClient()
        self.deferred = defer.Deferred()
        self.setRounds()
        self.crops = {'world':(-180.0, 90.0, 180.0, -90.0),
                      'us':(-125, 52, -65, 22),
                      'europe':(-25, 72, 51, 34)
                  }
        
    def setRounds(self):
        self.gameOver = False
        self.rounds = ['africa', 'world capitals', 'world', 'us', 'europe']
        self.roundNumber = 0
        
        
    def start(self):
        self.nextRound("Choose the position of the given city.  If you miss by more than %i km, the round is over" % self.maximumDistance)
        reactor.run()
        
    def quit(self):
        reactor.stop()
    
    
    def mouseEvent(self, event):
        if self.landmarks == None or len(self.landmarks) == 0 or self.landmark == None:
            print 'do nothing'
        elif not self.timeLoop.running:
            self.nextRound("Sorry, you didn't guess in time")
        elif self.timeLoop.running:
            print 'running'
            self.timeLoop.stop()
            answer = (event.x, event.y)
            distance = self.map.getDistance(answer, self.landmark)
            if self.worstGuess is None:
                self.worstGuess = distance
            elif distance > self.worstGuess:
                self.worstGuess = distance
            self.view.deleteLines()
            self.view.drawLines('blue', (event.x, event.y))
            x, y = self.map.mapToScreen(self.landmark['lat'], self.landmark['long'])
            self.view.drawLines('red', (x, y))
            self.view.drawCircle('red', (x, y), 25)
            self.view.answer.set("Distance: %d km" % int(distance))
            if distance > self.maximumDistance:
                self.nextRound("Sorry, you missed by more than %i km" % self.maximumDistance)
            else:
                self.view.nextRound.set('%i questions left' % len(self.landmarks))       
                time = self.time
                # calculate score
                score = self.calculateScore(time, distance)
                self.score += score
                self.view.scoreText.set("Total Score: %i" % int(self.score))
                self.view.showMessage("Score: %i Total: %i" % (int(score),  int(self.score)))
                self.getQuestion()
                              
                
    def nextRound(self, message):
        if len(self.rounds) > 0:
            self.landmarks = None
            round = self.rounds.pop()
            crop = self.crops[round]
            self.map.crop(crop)
            self.view.makeImage()
            self.roundNumber += 1
            message = message + "\n\nRound %i\n%s: The 50 most populus cities" % (self.roundNumber, round.capitalize())
            try:
                self.getLandmarks(round)
            except ConnectionError:
                self.view.showMessage("Sorry, the stupid game server is not running.  Quitting game NOW!")
                self.quit()
            self.view.showMessage(message)
            self.getQuestion()
        else:
            self.gameOver = True
            self.view.showMessage("Game over, now attempting to post your score to the server")
            try:
                self.postScore()
            except ConnectionError:
                self.view.showMessage("Sorry, the stupid game server is not running.  Quitting game NOW!")
                self.quit()
        
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
            self.gameOver = False
            
    def postScore(self):
        name = self.view.nameInput.get()
        if name == '':
            name = 'anonymous'
        data = "%s %i %.1f" % (name, int(self.score), float(self.worstGuess))
        listOfScores = self.client.addScore(data)
        scores = "High Scores: \n"
        scores += listOfScores
        self.view.scoresText.set(scores)
        self.view.showScores(scores)
        
    def getLandmarks(self, difficulty):
        try:
            self.landmarks = self.client.getLandmarks(difficulty)
        except ConnectionError:
            self.view.showMessage("Sorry, the stupid game server is not running.  Quitting game NOW!")
            self.quit()
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
        #self.view.updateNextRoundBar(score)
        return score

def main():
    g = Geography()
    g.start()

if __name__ == "__main__":
    main()
        
