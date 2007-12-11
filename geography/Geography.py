import math
import pickle
import random
import datetime

class Coords:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        
class Landmark:
    def __init__(self, name=None, country=None, coords=None):
        self.name = name
        self.country = country
        self.coords = coords


class GeographyMachine:
    def __init__(self):
        #self.landmark = Landmark("Denver", Coords(39.64 ,-104.90))
        #self.landmark = Landmark("Salt Lake", Coords(40.04 ,-112.4))
        #self.landmark = Landmark("Hawaii", Coords(19.47, -155.46))
        pkl_file = open('data/data.pkl', 'rb')

        self.landmarks = pickle.load(pkl_file)
        self.landmarks = self.landmarks.values()
        
        pkl_file.close()
        
        
    def getLandmark(self):
        l = len(self.landmarks)
        if l > 0:
            d = datetime.datetime.now()
            d = d.microsecond
            random.seed(d)
            i = random.randint(0, l - 1)
            self.landmark = self.landmarks.pop(i)
            return self.landmark
        return None
    
    def checkAnswer(self, answer):
        distance = self.getDistance(answer)
        return distance
        
        
    def getDistance(self, answer):
        R = 6371
        lat1 = math.radians(answer.lat)
        lat2 = math.radians(self.landmark.coords.lat)
        long1 = math.radians(answer.long)
        long2 = math.radians(self.landmark.coords.long)
        dLat = lat2 - lat1
        dLong = long2 - long1
        a = (math.sin(dLat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dLong/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return math.floor(d)
    
    