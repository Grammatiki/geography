import math
import pickle
import random
import datetime
from server.Landmark import Coords
from PIL import Image

class Map:
    def __init__(self, imageFile, screenSize=None):
        self.image = Image.open(imageFile)
        self.screenSize = screenSize
        if screenSize != None:
            self.screenWidth, self.screenHeight = screenSize
        
    def crop(self, boundries):
        self.left, self.top, self.right, self.bottom = boundries
        crop = self.convertCrop(boundries)
        self.croppedImage = self.image.crop(crop)
        if self.screenSize != None:
            self.croppedImage = self.croppedImage.resize((self.screenWidth, self.screenHeight), Image.BICUBIC)
            
    def saveCroppedImage(self, filename):
        self.croppedImage.save(filename)
                  
    def getDistance(self, answer, landmark):
        print 'get distance', answer, landmark
        R = 6371
        lat1, long1 = self.screenToMap(answer[0], answer[1])
        print lat1, long1
        lat1 = math.radians(lat1)
        lat2 = math.radians(landmark['lat'])
        long1 = math.radians(long1)
        long2 = math.radians(landmark['long'])
        dLat = lat2 - lat1
        dLong = long2 - long1
        a = (math.sin(dLat/2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(dLong/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return math.floor(d)
    
    def screenToMap(self, x, y):
        yRise = float(self.bottom - self.top)
        xRise = float(self.right - self.left)
        lat = float(yRise/self.screenHeight) * y + self.top
        long = float(xRise/self.screenWidth) * x + self.left
        print 'lat, long', lat, long
        #print lat, long
        #x = x - self.mapSize[0]/2
        #y = (-1 * y) + self.mapSize[1]/2
        #lat = y * 90.0 / (self.mapSize[1]/2)
        #long = x * 180.0 / (self.mapSize[0]/2)
        #print lat, long
        return lat, long
    
    def mapToScreen(self, lat, long):
        yRise = -1 * self.screenHeight
        yRun = self.top - self.bottom
        ySlope = yRise / yRun
        yIntercept = self.screenHeight - (ySlope * self.bottom)
        y = int((lat * ySlope) + yIntercept)
        
        xRise = self.screenWidth
        xRun = self.right - self.left
        xSlope = xRise / xRun
        xIntercept = self.screenWidth - (xSlope * self.right)
        x = int((long * xSlope) + xIntercept)
        
        #print 'x', x
        #x = (long * self.screenWidth/2) / 180
        #y = (lat * self.screenHeight/2) / 90
        #x = int(x + self.screenWidth/2)
        #y = int(self.screenHeight/2 - y)
        print 'x', x
        return x, y
    
    def convertCrop(self, crop):
        #convert the crop (which is in latitude and longitude) to pixels.
        left, top, right, bottom = crop
        width, height = self.image.size
        print self.image.size
        yRise = float(-1 * height)
        xRise = float(width)
        print 'slope', top * yRise/180.0
        print 'yrise', yRise
        y1 = int((top * (yRise/180.0)) + height / 2)
        y2 = int(bottom * (yRise/180.0) + height / 2)
        x1 = int(left * (xRise/360.0) + width / 2)
        x2 = int(right * (xRise/360.0) + width/ 2)
        print crop
        print x1, y1, x2, y2
        return x1, y1, x2, y2
    
    
    
    
