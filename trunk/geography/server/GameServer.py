from twisted.spread import pb
from GameScores import GameScores

class GamePerspective(pb.Root):
    def __init__(self, gameScores):
        self.gameScores = gameScores
        
    def remote_getScores(self):
        return self.gameScores.getScores()
    
    def remote_getLandmarks(self):
        return self.gameScores.getLandmarks()
    
    def remote_addScore(self, score):
        self.gameScores.addScore(score)

if __name__ == "__main__":
    import sys
    from twisted.internet import reactor
    gameScores = GameScores()
    gamePerspective = GamePerspective(gameScores)
    reactor.listenTCP(8789, pb.PBServerFactory(gamePerspective))
    reactor.run()
