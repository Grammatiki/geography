from twisted.spread import pb
from GameData import GameData

class GamePerspective(pb.Root):
    def __init__(self, gameData):
        self.gameData = gameData
        
    def remote_getScores(self):
        return self.gameData.getData()
    
    def remote_getLandmarks(self, difficulty):
        return self.gameData.getLandmarks(difficulty)
    
    def remote_addScore(self, score):
        self.gameData.addScore(score)

if __name__ == "__main__":
    import sys
    from twisted.internet import reactor
    gameData = GameData()
    gamePerspective = GamePerspective(gameData)
    reactor.listenTCP(8387, pb.PBServerFactory(gamePerspective))
    reactor.run()
