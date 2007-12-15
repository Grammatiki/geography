

class GameScores:
    def __init__(self):
        self.scores = {}
        self.worstGuess = {}
        
    def addScore(self, score):
        print "Adding Score", score
        name, score = score.split()
        print name, score
    
    def getScores(self):
        return "here are the scores"
    
    def getWorstGuess(self):
        return "Here is the worst guess"
