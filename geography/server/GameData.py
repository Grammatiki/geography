from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Landmark import Landmark, Coords
import random
import datetime
import pickle

class Scores(dict):
    def __init__(self):
        self.worstGuess = {'distance':0, 'name':''}
        
    def __setitem__(self, score, name):
        if self.has_key(score):
            self.pop(score)
            dict.setdefault(self, score, name)
        elif len(self) < 10:
            dict.setdefault(self, score, name)
        else:
            min = self.getMin()
            if score >= min:
                self.pop(min)
                dict.setdefault(self, score, name)
                
    def addWorstGuess(self, distance, name):
        if distance >= self.worstGuess['distance']:
            self.worstGuess = {'name':name, 'distance':distance}
    
    def addBestGuess(self, guess):
        pass
    
    def getScores(self):
        scores = []
        returnString = ''
        for key in self.iterkeys():
            scores.append(key)
        scores.sort(reverse=True)
        for score in scores:
            returnString += "%.1f\t%s\n" % (score, self[score])
        returnString += "\nAll time worst guess: %.1f km by %s\n" % (self.worstGuess['distance'], self.worstGuess['name'])
        return returnString
    
    def getMin(self):
        min = None
        for key in self.iterkeys():
            if min == None:
                min = key
            if key < min:
                min = key
        return min
                
                

class GameData:
    def __init__(self):
        try:
            f = open("data/scores.pkl", 'wb')
            self.scores = pickle.load(f)
        except Exception:
            self.scores = Scores()
            
        query = "select l.landmark_name, l.latitude, l.longitude, c.country_name from landmarks l, countries c"
        self.queries = {'world capitals' : query + " where c.id = l.country_id and c.capital_id not null and c.capital_id = l.id order by l.population",
                        'us' : query + " where c.id = l.country_id and c.country_name = 'United states' order by l.population",
                        'africa': query + ", africa a where c.id = l.country_id and c.id = a.country_id and l.population > 1000000 order by l.population",
                        'europe': query + ", europe e where c.id = l.country_id and c.id = e.country_id and l.population > 1000000 order by l.population",
                        'world' : query + " where c.id = l.country_id and l.population > 1000000 order by l.population"
                        }
        
        
    def loadLandmarks(self, keyword):
        engine = create_engine('sqlite:///data/landmarks.db')
        connection = engine.connect()
        query = self.queries[keyword]
        result = connection.execute(query)
        returnList = []
        for row in result:
            returnList.append({'name':row['landmark_name'], 'country':row['country_name'],'lat':row['latitude'], 'long':row['longitude']})
        connection.close()
        return returnList
        
    

    def getLandmarks(self, keyword):
        returnList = self.loadLandmarks(keyword)
        return returnList[-50:]
    
    def addScore(self, score):
        name, score, worstGuess = score.split()
        score = int(score)
        worstGuess = float(worstGuess)
        self.scores[score] = name
        self.scores.addWorstGuess(worstGuess, name)
        f = open('data/scores.pkl', 'wb')
        pickle.dump(self.scores, f)
        f.close()
    
    def getScores(self):
        return self.scores.getScores()
    
        
    
        
