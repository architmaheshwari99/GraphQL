from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher

from config.config import DB_URL
from db.data import employers_data, jobs_data, users_data, job_applications
from db.models import Employer, Job, Base, User, JobApplication

engine = create_engine(DB_URL, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
ph = PasswordHasher()

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

    for user in users_data:
        user["password_hash"] = ph.hash(user['password'])
        del user['password']
        session.add(User(**user))

    for job_application in job_applications:
        session.add(JobApplication(**job_application))

    session.commit()
    session.close()
