from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Landmark import Landmark, Coords
import random
import datetime

class GameData(dict):
    def __init__(self):
        self.worstGuess = (None, None)
        self.landmarks = {'easy':[], 'medium':[], 'difficult':[]}
        self.loadLandmarks('easy')
        self.loadLandmarks('medium')
        self.loadLandmarks('difficult')
        
        
    def loadLandmarks(self, difficulty):
        engine = create_engine('sqlite:///data/landmarks.db')
        connection = engine.connect()
        query = "select * from landmarks where difficulty='%s'" % difficulty
        result = connection.execute(query)
        self.landmarks[difficulty] = []
        for row in result:
            self.landmarks[difficulty].append({'name':row['name'], 'country':row['country'], 'lat':row['latitude'], 'long':row['longitude']})
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
        self.returnList = []
        for i in range(20):
            l = len(self.landmarks[difficulty])    
            if l > 0:
                self._getLandmark(difficulty, l)
            else:
                self.loadLandmarks(difficulty)
                self._getLandmark(difficulty, 20)
        print returnList
        return self.returnList
            
    def _getLandmark(self, difficulty, l):
        d = datetime.datetime.now()
        d = d.microsecond
        random.seed(d)
        r = random.randint(0, l - 1)
        self.returnList.append(self.landmarks[difficulty].pop(r))
        
    
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
        
