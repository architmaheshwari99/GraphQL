from graphene import ObjectType, String, Int, List, Field
from sqlalchemy.orm import joinedload

from db.database import Session
from db.models import Job, Employer, User, JobApplication


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
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


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()


class JobApplicationObject(ObjectType):
    id = Int()
    job_id = Int()
    user_id = Int()
    job = Field(JobObject)
    user = Field(UserObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user

    @staticmethod
    def resolve_job(root, info):
        return root.job
