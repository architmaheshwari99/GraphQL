from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import DB_URL
from db.data import employers_data, jobs_data
from db.models import Employer, Job, Base

engine = create_engine(DB_URL)
conn = engine.connect()


def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))

    session.commit()
    session.close()
