from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, name, age):
        user = {"id": len(Query.users)+1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Adam Smith", "age": 34},
        {"id": 3, "name": "Adam Smith", "age": 35},
        {"id": 4, "name": "Adam Smith", "age": 36}
    ]

    def resolve_user(self, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else {"id": 4, "name": "Adam Smith", "age": 36}

    def resolve_users_by_min_age(self, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]

schema = Schema(query=Query, mutation=Mutation)


gql_1 = '''
mutation {
    createUser(name:"Archit", age: 35){
        user {
            id
            name
            age
        }
    }
}
'''


gql_2 = '''
query {
    user(userId: 5){
        id
        name
        age
    }
}
'''



if __name__ == '__main__':
    res = schema.execute(gql_1)
    print(res)
    res = schema.execute(gql_2)
    print(res)
