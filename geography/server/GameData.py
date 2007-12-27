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

        query = "select l.landmark_name, l.latitude, l.longitude, c.country_name from landmarks l, countries c"
        self.queries = {'capitals' : query + "where c.id = l.country_id and c.capital_id not null and c.capital_id = l.id",
                        'us' : query + " where c.id = l.country_id and c.country_name = 'United states' order by l.population",
                        'africa':None,
                        'europe': query + ", europe e where c.id = l.country_id and c.id = europe.country_id order by l.population",
                        'world' : query + " where c.id = l.country_id and l.population > 1000000 order by l.population"
                        }
        
        
    def loadLandmarks(self, keyword):
        engine = create_engine('sqlite:///data/landmarks.db')
        connection = engine.connect()
        query = self.queries[keyword]
        print query
        result = connection.execute(query)
        returnList = []
        for row in result:
            returnList.append({'name':row['landmark_name'], 'country':row['country_name'],'lat':row['latitude'], 'long':row['longitude']})
        connection.close()
        return returnList
        
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
        returnList = self.loadLandmarks(keyword)
        return returnList[-50:]
            
    
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
        
