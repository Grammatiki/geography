from twisted.spread import pb
from twisted.internet import reactor

class GameClient(object):
    def __init__(self):
        self.scores = None

    def connect(self):
        factory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 8387, factory)
        return factory.getRootObject().addCallback(self._connected)

    def _connected(self, rootObj):
        print rootObj
        self.data = rootObj

    def getLandmarks(self, difficulty):
        print "Getting landmarks"
        return self.data.callRemote('getLandmarks', difficulty).addCallback(
            self._gotLandMarks)
    
    def _gotLandMarks(self, landmarks):
        self.landmarks = landmarks
        print "Got landmarks"
        
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
