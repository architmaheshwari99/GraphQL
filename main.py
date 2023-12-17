from graphene import Schema, ObjectType, String


class Query(ObjectType):
    hello = String(name=String(default_value='world'))

    def resolve_hello(self, info, name):
        return f"Hello {name}"


schema = Schema(query=Query)

gql = '''
{
    hello(name: "graphQL")
}
'''

if __name__ == '__main__':
    res = schema.execute(gql)
    print(res)
