import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from graphene import Mutation, String, Int, Field, ObjectType, Boolean
from graphql import GraphQLError

# from config.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES
from db.database import Session
from db.models import Job, Employer, User, JobApplication
from gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject

ph = PasswordHasher()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME_MINUTES = os.getenv("TOKEN_EXPIRATION_TIME_MINUTES")


def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def admin_user(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != 'admin':
            raise GraphQLError('You are not authorized')
        resp = fn(*args, **kwargs)
        return resp
    return inner

def authd_user(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get('user_id')
        if user.id != uid:
            raise GraphQLError('You are not authorized')
        resp = fn(*args, **kwargs)
        return resp
    return inner

def authenticated_user(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)
        resp = fn(*args, **kwargs)
        return resp

    return inner


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    @admin_user
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


def get_authenticated_user(context):
    """
    {
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYmMxIiwiZXhwIjoxNzAzNjEyMDUwfQ.jUQptBU2LvUKWg_AnMvdVDMCpVe73ewqkoKI3y9t12w",
    }

    :param context:
    :return:
    """
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')
    print(request_object.headers, auth_header)
    if auth_header:
        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz = timezone.utc):
                raise GraphQLError('Token has expired')

            session = Session()
            user = session.query(User).filter(User.email == payload.get("sub")).first()

            if not user:
                raise GraphQLError('User not found')

            return user
        except jwt.exceptions.InvalidSignatureError:
            raise GraphQLError('Invalid Authentication token')
    else:
        raise GraphQLError('No auth token')


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(EmployerObject)

    authenticated_as = Field(String)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        user = get_authenticated_user(info.context)
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        session.close()
        return AddEmployer(employer=employer, authenticated_as=user.email)


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
        employer = session.query(Employer).filter(Employer.id == id).first()
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
    @admin_user
    @staticmethod
    def mutate(root, info, employer_id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == employer_id).first()
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

        token = generate_token(email)

        return LoginUserMutation(token=token)


class AddUserMutation(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(UserObject)

    @staticmethod
    def mutate(root, info, email, password, role):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise GraphQLError('Email already in use')

        user = get_authenticated_user(info.context)
        if role == 'admin' and user.role!='admin':
            raise GraphQLError('Admin role cannot be assigned')


        user = User(email=email, password_hash=ph.hash(password), role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return AddUserMutation(user=user)


class ApplyToJobMutation(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    application = Field(JobApplicationObject)


    @staticmethod
    @authd_user
    def mutate(root, info, user_id, job_id):
        session = Session()
        application = session.query(JobApplication).filter(JobApplication.user_id==user_id, JobApplication.job_id==job_id).first()
        if application:
            raise GraphQLError('Already applierd to the job')

        application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(application)
        session.commit()
        session.refresh(application)

        return ApplyToJobMutation(application)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUserMutation.Field()
    add_user = AddUserMutation.Field()
    apply_to_job = ApplyToJobMutation.Field()