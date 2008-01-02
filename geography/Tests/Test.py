from Map import Map
from Parser import Parser
import math

class Map:
    def setup(self):
        self.map = Map((1, 2), 'image.jpg')
        
    def testGetDistance(self):
        self.geographyMachine.landmark = Landmark( name="Denver", coords=Coords(39.64 ,-104.90))
        answer = Coords(45.64, -122.68)
        distance = self.geographyMachine.getDistance(answer)
        assert distance == 1595, "Actual answer: %f" % distance
        
class _TestParser:
    def setup(self):
        self.parser = Parser()
        
    def _testReadFile(self):
        self.parser.parse()
        