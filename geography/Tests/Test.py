from Geography import GeographyMachine, Landmark, Coords
from Parser import Parser
import math

class TestGeographyMachine:
    def setup(self):
        self.geographyMachine = GeographyMachine()
    def testGetDistance(self):
        self.geographyMachine.landmark = Landmark( name="Denver", coords=Coords(39.64 ,-104.90))
        answer = Coords(45.64, -122.68)
        distance = self.geographyMachine.getDistance(answer)
        assert distance == 1595, "Actual answer: %f" % distance
        
class TestParser:
    def setup(self):
        self.parser = Parser()
        
    def testReadFile(self):
        self.parser.parse()
        