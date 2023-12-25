from graphene import ObjectType, String, Int, List, Field
from sqlalchemy.orm import joinedload

from db.database import Session
from db.models import Job, Employer


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_name = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        session = Session()
        jobs_data = session.query(Job).filter(Job.employer_id==root.id)
        session.close()
        return jobs_data


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        session = Session()
        employers_data = session.query(Employer).filter(Employer.id == root.employer_id).first()
        session.close()
        return employers_data
