from sqlalchemy import create_engine, select, insert
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey

dataFile = open('europe.txt', 'r')

db = create_engine('sqlite:///landmarks.db', echo=False)
metadata = MetaData()
europe = Table('europe', metadata,
               Column('id', Integer, primary_key=True),
               Column('country_id', String(60)),
           )

metadata.create_all(db)
metadata.bind = db
for line in dataFile.readlines():
    country = line.strip()
    query = "select c.id from countries c where c.country_name = '%s'" % country
    result = db.execute(query)
    row = result.fetchone()
    result.close()
    if row != None:
        europe.insert().execute(country_id=row['id'])

dataFile.close()
