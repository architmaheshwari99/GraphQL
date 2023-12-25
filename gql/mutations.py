from graphene import Mutation, String, Int, Field, ObjectType
from sqlalchemy.orm import joinedload

from db.database import Session
from db.models import Job
from gql.types import JobObject


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job)

        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, job_id, title, description, employer_id):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        #  Avoid lazy loading
        # job = session.query(Job).options(joinedload(Job.employer))\
        #     .filter(Job.id == job_id).first()
        if not job:
            raise Exception('Job not found')

        if title:
            job.title = title
        if description:
            job.description = description
        if employer_id:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job)
        return UpdateJob(job=job)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
