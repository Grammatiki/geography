class Coords:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        
class Landmark(object):
    def __init__(self, name=None, country=None, coords=None, difficulty=None, population=None):
        self.name = name
        self.country = country
        self.population = population
        self.difficulty = difficulty
        self.latitude = coords.lat
        self.longitude = coords.long