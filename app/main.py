from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler

from db.database import prepare_database
from gql.queries import Query

schema = Schema(query=Query)
app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
app.mount("/graphql-p", GraphQLApp(schema=schema, on_get=make_playground_handler()))
