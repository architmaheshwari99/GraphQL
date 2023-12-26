import string
from random import choices

from argon2.exceptions import VerifyMismatchError
from graphene import Mutation, String, Int, Field, ObjectType, Boolean
from graphql import GraphQLError
from sqlalchemy.orm import joinedload

from db.database import Session
from db.models import Job, Employer, User
from gql.types import JobObject, EmployerObject

from argon2 import PasswordHasher

ph = PasswordHasher()


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


class DeleteJob(Mutation):
    class Arguments:
        job_id = Int(required=True)

    result = Boolean()

    @staticmethod
    def mutate(root, info, job_id):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise Exception('Job not found')

        session.delete(job)
        session.commit()
        session.close()

        return DeleteJob(result=True)


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(EmployerObject)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        session.close()
        return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(EmployerObject)


    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        session = Session()
        employer = session.query(Employer).filter(Employer.id==id).first()
        if not employer:
            raise Exception('Employer not found')

        if name:
            employer.name = name
        if contact_email:
            employer.contact_email = contact_email
        if industry:
            employer.industry = industry

        session.commit()
        session.refresh(employer)
        session.close()
        return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)

    result = Boolean()

    @staticmethod
    def mutate(root, info, employer_id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id==employer_id).first()
        if not employer:
            raise Exception('Employer not found')
        session.delete(employer)
        session.commit()
        session.close()

        return DeleteEmployer(result=True)


class LoginUserMutation(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError('Invalid email')

        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise GraphQLError('Invalid Password')


        token = ''.join(choices(string.ascii_lowercase, k=10))

        return LoginUserMutation(token=token)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUserMutation.Field()

