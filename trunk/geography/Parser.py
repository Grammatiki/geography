import re
import pickle
from server.Landmark import Landmark, Coords
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

class Parser:
    def __init__(self):
        self.dataFile = open('server/data/worldcitiespop.txt')
        self.countriesFile = open('server/data/countries.txt')
        #self.data = {'easy':[],'medium':[], 'difficult':[]}
    
    
    def parse(self):
        countries = {}
        for line in self.countriesFile.readlines():
            key = line[:2].lower()
            value = line[3:]
            value = value.replace('\"', '')
            value = value.strip()
            value = value.capitalize()
            countries[key] = value
            print key
            
        #engine = create_engine('sqlite:///:memory:', echo=False)
        engine = create_engine('sqlite:///landmarks.db', echo=False)
        metadata = MetaData()
        landmarks_table = Table('landmarks', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(60)),
                    Column('country', String(50)),
                    Column('population', Integer),
                    Column('difficulty', String(15)),
                    Column('latitude', Float),
                    Column('longitude', Float)
                    )
        metadata.create_all(engine)


        mapper(Landmark, landmarks_table)
        Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
        session = Session()

        
        self.dataFile.readline() #get rid of the header line
        i = 0
        for line in self.dataFile.readlines():
            line = line.strip()
            country, city, accentCity, region, population, lat, long = line.split(',')
            if population != '':
                population = int(population)
                country = countries[country]
                city = city.capitalize()
                lat = float(lat)
                long = float(long)
                if population < 300000:
                    difficulty = 'difficult'
                elif population >= 300000 and population < 1000000:
                    difficulty = 'medium'
                elif population >= 1000000:
                    difficulty = 'easy'
                coords = Coords(lat, long)
                landmark = Landmark(name=city, country=country, coords=coords, difficulty=difficulty, population=population)
                session.save(landmark)
                i += 1
                if i == 5:
                    i = 0
                    session.commit()
        
                
                    
        #output = open('data/worldcitiespop.pkl', 'wb')

        # Pickle dictionary using protocol 0.
        #pickle.dump(self.data, output)
        #output.close()
        self.dataFile.close()
        
            
        
parser = Parser()
parser.parse()

