

class GameScores(dict):
    def __init__(self):
        self.worstGuess = {}
        
    def __setitem__(self, key, value):
        if self.has_key(key):
            self.pop(key)
            dict.setdefault(self, key, value)
        elif len(self) < 10:
            dict.setdefault(self, key, value)
        else:
            min = self.getMin()
            if key >= min:
                self.pop(min)
                dict.setdefault(self, key, value)
                
        
    def addScore(self, score):
        print "Adding Score", score
        score, name = score.split()
        score = float(score) 
        self[score] = name
    
    def getScores(self):
        scores = []
        returnString = ''
        for key in self.iterkeys():
            scores.append(key)
        scores.sort(reverse=True)
        for score in scores:
            returnString += "%.1f\t%s\n" % (score, self[score])
        return returnString
    
        
    def getMin(self):
        min = 1000000000
        for key in self.iterkeys():
            if key < min:
                min = key
        return min
        
    
    def getWorstGuess(self):
        return "Here is the worst guess"
