from graphene import Schema, ObjectType, String
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler


class Query(ObjectType):
    pass


schema = Schema(query=Query)
app = FastAPI()

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
app.mount("/graphql-p", GraphQLApp(schema=schema, on_get=make_playground_handler()))
