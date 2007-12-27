from sqlalchemy import create_engine, select, insert
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey



dataFile = open('capitals.txt')
db = create_engine('sqlite://landmarks.db', echo=False)
metadata = MetaData()
capitals_table = Table('capitals', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('cityId', Integer),
                                Column('countryId', Integer)
                                )

metadata.create_all(db)
metadata.bind = db

conn = db.connect()
for line in dataFile.readlines():
    country, capital = line.split(" - ")
    country = country.strip()
    capital = capital.split()
    query = "select countries.id, landmarks.id from countries, landmarks where countries.country=='%s' and countries.id==landmarks.countryId" % country
    result = conn.execute(query)
    row = result.fetchone()
    if row != None:
        capitals_table.insert().execute(cityId=row[1], countryId=row[0])

dataFile.close()
