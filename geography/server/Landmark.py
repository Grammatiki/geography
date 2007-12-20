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