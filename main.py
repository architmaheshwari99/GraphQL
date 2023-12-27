from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler

from db.database import prepare_database, Session
from db.models import Employer, Job, JobApplication
from gql.mutations import Mutation
from gql.queries import Query

schema = Schema(query=Query, mutation=Mutation)
app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()


@app.get("/employers")
def get_employers():
    session = Session()
    employers = session.query(Employer).all()
    session.close()
    return employers


@app.get("/jobs")
def get_jobs():
    session = Session()
    jobs = session.query(Job).all()
    session.close()
    return jobs

@app.get("/apps")
def get_applications():
    with Session() as session:
        return session.query(JobApplication).count()

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
