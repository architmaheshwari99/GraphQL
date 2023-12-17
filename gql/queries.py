from graphene import ObjectType, List

from db.data import jobs_data, employers_data
from gql.types import EmployerObject, JobObject


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data

