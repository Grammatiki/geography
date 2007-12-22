from twisted.spread import pb
from twisted.internet import reactor
from ReconnectingPBClientFactory import ReconnectingPBClientFactory

class GameClient(object):
    def __init__(self):
        self.scores = None
        self.data = None
        self.factory = ReconnectingPBClientFactory()

    def connect(self):        
        reactor.connectTCP("localhost", 8387, self.factory)
        print dir(self.factory)
        #return self.factory.getRootObject().addCallback(self._connected)

    def _connected(self, rootObj):
        print rootObj
        self.data = rootObj

    def getLandmarks(self, difficulty):
        if self.data == None:
            self.data = self.factory.data
        return self.data.callRemote('getLandmarks', difficulty).addCallback(
            self._gotLandMarks)
    
    def _gotLandMarks(self, landmarks):
        self.landmarks = landmarks
        print "Got landmarks", landmarks
        
    def getScores(self):
        print "Getting scores..."
        return self.data.callRemote('getScores').addCallback(
            self._gotScores)
    
    def _gotScores(self, scores):
        self.listOfScores = scores
        print "Got scores:", scores
        
    def addScore(self, score):
        return self.data.callRemote('addScore', score)

    def _catchFailure(self, failure):
        print "Error:", failure.getErrorMessage()


#t = GameClient()
#t.getInfo()
#reactor.run()
