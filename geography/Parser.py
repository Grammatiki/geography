import re
import pickle
from Geography import Landmark, Coords

class Parser:
    def __init__(self):
        self.dataFile = open('data/data.txt')
        self.data = {'easy':[],'medium':[], 'difficult':[]}
    
    def parse(self):
        for line in self.dataFile.readlines():
            line = line.strip()
            if len(line) > 0:
                p = re.compile('\d')
                if p.search(line):
                    self.parsePlace(line)
                else:
                    self.country = line.strip()
                    
        output = open('data/data.pkl', 'wb')

        # Pickle dictionary using protocol 0.
        pickle.dump(self.data, output)
        output.close()
        self.dataFile.close()
        
    def parsePlace(self, line):
        parts = line.split()
        coords = parts[-7:]
        name = parts[:-7]
        name = " ".join(name)
        coords, difficulty = self.parseCoords(coords)
        self.data[difficulty].append(Landmark(name=name, country=self.country, coords=coords, difficulty=difficulty))
        print self.data[difficulty]
        
        
    def parseCoords(self, coords):
        p = re.compile('\D')
        latNumber = coords[0]
        m = p.search(latNumber)
        latNumber = int(latNumber[:m.start()])
        
        latDecimal = coords[1]
        m = p.search(latDecimal)
        latDecimal = float(latDecimal[:m.start()]) / 60.0
        latDecimal = latDecimal
        
        lat = latNumber + latDecimal
        
        hemi = coords[2]
        if hemi == 'S':
            lat *= -1
        
        
        longNumber = coords[3]
        m = p.search(longNumber)
        longNumber = int(longNumber[:m.start()])
        
        longDecimal = coords[4]
        m = p.search(longDecimal)
        longDecimal = float(longDecimal[:m.start()]) / 60.0
        
        long = longNumber + longDecimal

        hemi = coords[5]
        if hemi == 'W':
            long *= -1
            
        difficulty = coords[6]
            
        return Coords(lat, long), difficulty
            
        
parser = Parser()
parser.parse()

