from graphene import Schema, ObjectType, String, Int, Field


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())

    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Adam Smith", "age": 34},
        {"id": 3, "name": "Adam Smith", "age": 35},
        {"id": 4, "name": "Adam Smith", "age": 36}
    ]

    def resolve_user(self, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else {"id": 4, "name": "Adam Smith", "age": 36}


schema = Schema(query=Query)

gql = '''
query {
    user(userId: 2){
        id
        name
        age
    }
}
'''

if __name__ == '__main__':
    res = schema.execute(gql)
    print(res)
