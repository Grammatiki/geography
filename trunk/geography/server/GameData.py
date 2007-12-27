from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Landmark import Landmark, Coords
import random
import datetime
import pickle

class GameData(dict):
    def __init__(self):
        self.worstGuess = (None, None)
        self.bestGuess = (None, None)
        self.landmarks = {'easy':[],
                          'capitals':[],
                          'us':[],
                          'europe':[],
                          'africa':[],
                      }
        query = "select l.landmark_name, l.latitude, l.longitude, c.country_name from landmarks l, countries c where c.id = l.country_id"
        self.queries = {'easy': query + "l.population > 2000000",
                        'capitals' : query + " and c.capital_id not null and c.capital_id = l.id",
                        'us' : query + " and c.country_name = 'United states' and l.population > 400000",
                        'europe': None,
                        'africa':None,
                        'europeTopTwenty': "select l.landmark_name, l.latitude, l.longitude, c.country_name from landmarks l, countries c, europe e where c.id = l.country_id and c.id = europe.country_id order by l.population desc"
                        }
        
        
    def loadLandmarks(self, keyword):
        engine = create_engine('sqlite:///data/landmarks.db')
        connection = engine.connect()
        query = self.queries[keyword]
        result = connection.execute(query)
        if not self.landmarks.has_key(keyword):
            self.returnList = []
            for row in result:
                self.landmarks[keyword].append({'name':row['landmark_name'], 'country':row['country_name'],'lat':row['latitude'], 'long':row['longitude']})
                return returnList
        self.landmarks[keyword] = []
        for row in result:
            self.landmarks[keyword].append({'name':row['landmark_name'], 'country':row['country_name'],'lat':row['latitude'], 'long':row['longitude']})
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

    def getLandmarks(self, keyword):
        self.returnList = []
        if not self.landmarks.has_key(keyword):
            returnList = self.loadLandmarks(keyword)
            return returnList[:20]
        for i in range(20):
            l = len(self.landmarks[keyword])    
            if l > 0:
                self._getLandmark(keyword, l)
            else:
                self.loadLandmarks(keyword)
                self._getLandmark(keyword, 20)
        return self.returnList
            
    def _getLandmark(self, keyword, l):
        d = datetime.datetime.now()
        d = d.microsecond
        random.seed(d)
        r = random.randint(0, l - 1)
        self.returnList.append(self.landmarks[keyword].pop(r))
        print self.returnList
        
    
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
        
