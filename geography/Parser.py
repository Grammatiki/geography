import re
import pickle
from server.Landmark import Landmark, Coords
from sqlalchemy import create_engine, select, insert
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

class Parser:
    def __init__(self):
        self.dataFile = open('server/data/worldcitiespop.txt')
        self.countriesFile = open('server/data/countries.txt')
        #self.data = {'easy':[],'medium':[], 'difficult':[]}
    
    
    def parse(self):
        db = create_engine('sqlite:///server/data/landmarks.db', echo=False)
        metadata = MetaData()
        landmarks_table = Table('landmarks', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('landmark_name', String(60)),
                                Column('country_id', Integer),
                                Column('population', Integer),
                                Column('latitude', Float),
                                Column('longitude', Float)
                            )
        
        countries_table = Table('countries', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('country_name', String(60)),
                                Column('code', String(3)),
                                Column('capital_id', Integer)
                                )
        
        metadata.create_all(db)
        metadata.bind = db
        for line in self.countriesFile.readlines():
            key = line[:2].lower()
            value = line[3:]
            value = value.replace('\"', '')
            value = value.strip()
            value = value.capitalize()
            countries_table.insert().execute(country_name=value, code=key)

        self.countriesFile.close()
        #engine = create_engine('sqlite:///:memory:', echo=False)
        conn = db.connect()
        self.dataFile.readline() #get rid of the header line
        i = 0
        for line in self.dataFile.readlines():
            line = line.strip()
            country, city, accentCity, region, population, lat, long = line.split(',')
            if population != '':
                population = int(population)
                city = city.capitalize()
                lat = float(lat)
                long = float(long)
                query = select([countries_table.c.id])
                query = query.where(countries_table.c.code==country)
                result = conn.execute(query)
                row = result.fetchone()
                countryId = row[0]
                landmarks_table.insert().execute(landmark_name=city, country_id=countryId, population=population, latitude=lat, longitude=long)
                print countryId
                result.close()
                #result.close()
                #i += 1
                #if i == 5:
                    #i = 0
                    #session.commit()
        #metadata.bind = db
        
        conn = db.connect()
        dataFile = open('server/data/capitals.txt')
        for line in dataFile.readlines():
            country, capital = line.split(" - ")
            country = country.strip()
            capital = capital.strip()
            query = "select l.id, c.id from landmarks l, countries c where l.landmark_name='%s' and c.country_name = '%s'" % (capital, country)
            print query
            result = conn.execute(query)
            row = result.fetchone()
            print row
            result.close()
            if row != None and len(row) == 2:
                cityId = row[0]
                countryId = row[1]
                print cityId, countryId
                query = "update countries set capital_id = %i where id = %i" % (cityId, countryId)
                conn.execute(query)
                #ins = capitals.insert()
                #conn.execute(ins, cityId=cityId, countryId=countryId)
        
        dataFile.close()
                    
        #output = open('data/worldcitiespop.pkl', 'wb')

        # Pickle dictionary using protocol 0.
        #pickle.dump(self.data, output)
        #output.close()
        self.dataFile.close()
        
            
        
parser = Parser()
parser.parse()

