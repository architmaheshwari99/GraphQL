from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import DB_URL
from db.data import employers_data, jobs_data
from db.models import Employer, Job, Base

engine = create_engine(DB_URL, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


    for employer in employers_data:
        del employer["id"]
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        del job["id"]
        session.add(Job(**job))

    session.commit()
    session.close()
