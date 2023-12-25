from graphene import ObjectType, List, Field, Int

from db.data import jobs_data, employers_data
from db.database import Session
from db.models import Job, Employer, User, JobApplication
from gql.types import EmployerObject, JobObject, UserObject, JobApplicationObject


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)
    job = Field(JobObject, id=Int())
    employer = Field(EmployerObject, id=Int())
    users = List(UserObject)
    applications = List(JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        session = Session()
        job_applications = session.query(JobApplication).all()
        session.close()

        return job_applications


    @staticmethod
    def resolve_employer(root, info, id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == id).first()
        session.close()

        if employer:
            return employer
        return Exception('job not found')

    @staticmethod
    def resolve_jobs(root, info):
        session = Session()
        jobs_data = session.query(Job).all()
        session.close()
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        session = Session()
        employers = session.query(Employer).all()
        session.close()
        return employers


    @staticmethod
    def resolve_job(root, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        session.close()

        if job:
            return job
        return Exception('job not found')

    @staticmethod
    def resolve_users(root, info):
        session = Session()
        users = session.query(User).all()
        session.close()

        return users


"""
Fragments 
query {
  employer(id: 1) {
    ...employerFields
  }
}

fragment employerFields on EmployerObject {
  id name contactEmail industry jobs {
    ...jobFields
  }
}

fragment jobFields on JobObject {
  id title description employerId
}

"""