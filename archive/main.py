from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Adam Smith", "age": 34},
        {"id": 3, "name": "Adam Smith", "age": 35},
        {"id": 4, "name": "Adam Smith", "age": 36}
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]



class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users)+1, "name": name, "age": age}
        Query.users.append(user)
        # GraphQL schema expects the result of the mutation to be of the same type as mutation itself
        return CreateUser(user=user)


class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    # Output
    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        if not matched_users:
            return None
        user = matched_users[0]
        if name:
            user["name"] = name
        if age:
            user["age"] = age

        return UpdateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    result = Int()

    @staticmethod
    def mutate(root, info, user_id):
        matched_users = [(idx, user) for idx, user in enumerate(Query.users) if user["id"] == user_id]
        if not matched_users:
            return UpdateUser(result=False)
        user = matched_users[0]
        Query.users.remove(user[1])
        return DeleteUser(result=True)

class Mutation(ObjectType):
    # Think of this as a resolver for the mutation
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


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
mutation {
    updateUser(userId: 5, name: "Casper", age: 7){
        user {
            id
            name
            age
        }
    }
}
'''

delete_gql = '''
mutation {
    deleteUser(userId: 1){
        result
    }
}
'''

gql_3 = '''
query {
    user(userId: 5){
        id
        name
        age
    }
}
'''

gql_4 = '''
query {
    user(userId: 1){
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
    res = schema.execute(gql_3)
    print(res)
    res = schema.execute(delete_gql)
    print(res)
    res = schema.execute(gql_4)
    print(res)