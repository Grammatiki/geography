import math
import pickle
import random
import datetime
from server.Landmark import Coords

class Map:
    def __init__(self, screenSize, imageFile):
        self.image = Image.open(self.mapFile)
        self.screenWidth, self.screenHeight = screenSize
        self.image = image
        
    def crop(self, boundries):
        self.left, self.top, self.right, self.bottom = boundries
        crop = self.convertCrop(boundries)
        self.croppedImage = self.image.crop(crop)
        self.croppedImage = self.croppedImage.resize(self.mapSize, Image.BICUBIC)
                  
    def getDistance(self, answer, landmark):
        R = 6371
        lat1 = math.radians(answer.lat)
        lat2 = math.radians(landmark['lat'])
        long1 = math.radians(answer.long)
        long2 = math.radians(landmark['long'])
        dLat = lat2 - lat1
        dLong = long2 - long1
        a = (math.sin(dLat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dLong/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return math.floor(d)
    
    def convertCoords(self, x, y):
        yRise = (self.bottom - self.top)
        xRise = (self.right - self.left)
        lat = (yRise/self.height) * y + self.top
        long = (xRise/self.width) * x + self.left
        #print lat, long
        #x = x - self.mapSize[0]/2
        #y = (-1 * y) + self.mapSize[1]/2
        #lat = y * 90.0 / (self.mapSize[1]/2)
        #long = x * 180.0 / (self.mapSize[0]/2)
        #print lat, long
        return lat, long
    
    def convertCoordsBack(self, lat, long):
        rise = -1 * self.height
        y = lat * (rise/(self.top - self.bottom)) + self.height
        print 'y', y
        x = (long * self.width/2) / 180
        y = (lat * self.height/2) / 90
        x = int(x + self.width/2)
        y = int(self.height/2 - y)
        print 'y', y
        return x, y
    
    def convertCrop(self, crop):
        left, top, right, bottom = crop
        left, top = self.convertCoordsBack(top, left)
        right, bottom = self.convertCoordsBack(bottom, right)
        return left, top, right, bottom
    
    
    
    
