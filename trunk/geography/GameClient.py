from twisted.spread import pb
from twisted.internet import reactor

class GameClient(object):
    def __init__(self):
        self.scores = None

    def getInfo(self):
        self.connect().addCallback(
            lambda _: self.getScores()).addCallback(
            lambda _: self.getWorstGuess()).addErrback(
            self._catchFailure).addCallback(
            lambda _: reactor.stop())

    def connect(self):
        factory = pb.PBClientFactory()
        reactor.connectTCP("sabeto", 8789, factory)
        return factory.getRootObject().addCallback(self._connected)

    def _connected(self, rootObj):
        print rootObj
        self.scores = rootObj
        
    def getScores(self):
        print "Getting scores..."
        return self.scores.callRemote('getScores').addCallback(
            self._gotScores)
    
    def _gotScores(self, scores):
        self.listOfScores = scores
        print "Got scores:", scores

    def getWorstGuess(self):
        print "Getting worst guess..."
        return self.scores.callRemote('getWorstGuess').addCallback(
            self._gotWorstGuess)
    
    def _gotWorstGuess(self, worstGuess):
        self.worstGuess = worstGuess
        print "Got worst guess:", worstGuess
        
    def addScore(self, score):
        return self.scores.callRemote('addScore', score)

    def _catchFailure(self, failure):
        print "Error:", failure.getErrorMessage()


#t = GameClient()
#t.getInfo()
#reactor.run()
