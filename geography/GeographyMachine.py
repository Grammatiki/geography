import math
import pickle
import random
import datetime


class Coords:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        
class Landmark(object):
    def __init__(self, name=None, country=None, coords=None, difficulty=None, population=None):
        self.name = name
        self.country = country
        self.lat = coords.lat
        self.long = coords.long
        self.difficulty = difficulty
        self.population = population


class GeographyMachine:
                  
    def getDistance(self, answer, landmark):
        R = 6371
        lat1 = math.radians(answer.lat)
        lat2 = math.radians(landmark.coords.lat)
        long1 = math.radians(answer.long)
        long2 = math.radians(landmark.coords.long)
        dLat = lat2 - lat1
        dLong = long2 - long1
        a = (math.sin(dLat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dLong/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return math.floor(d)
    
    
