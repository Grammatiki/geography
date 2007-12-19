from sqlalchemy import create_engine
from sqlalchemy import sessionmaker
from GeographyMachine import Landmark

class GameData(dict):
    def __init__(self):
        self.worstGuess = (None, None)
        engine = create_engine('sqlite:///data/landmarks.db')
        connection = engine.connect()
        result = connection.execute("select * from landmarks where difficulty='easy'")
        self.easy = []
        for row in result:
            self.easy.append((row['name'], row['country']))
        
        result = connection.execute("select * from landmarks where difficulty='medium'")
        self.medium = []
        for row in result:
            self.medium.append((row['name'], row['country']))
        
        result = connection.execute("select * from landmarks where difficulty='difficult'")
        self.difficult = []
        for row in result:
            self.difficult.append((row['name'], row['country']))
        
        connection.close()

        
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
                
    def getLandmarks(self, difficulty):
        
    
    def addScore(self, score):
        print "Adding Score", score
        name, score, worstGuess = score.split()
        score = int(score)
        worstGuess = float(worstGuess)
        self[score] = name
        if worstGuess >= self.worstGuess[1]:
            self.worstGuess = (name, worstGuess)
    
    def getScores(self):
        scores = []
        returnString = ''
        for key in self.iterkeys():
            scores.append(key)
        scores.sort(reverse=True)
        for score in scores:
            returnString += "%.1f\t%s\n" % (score, self[score])
        returnString += "\nAll time worst guess: %.1f km by %s\n" % (self.worstGuess[1], self.worstGuess[0])
        return returnString
    
        
    def getMin(self):
        min = 1000000000
        for key in self.iterkeys():
            if key < min:
                min = key
        return min
        
    
    def getWorstGuess(self):
        return "%s  %.1f km" % (self.worstGuess[0], self.worstGuess[1])
