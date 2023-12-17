from graphene import ObjectType, List

from db.data import jobs_data, employers_data
from db.database import Session
from db.models import Job, Employer
from gql.types import EmployerObject, JobObject


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

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
