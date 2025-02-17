import graphene

class Person(graphene.ObjectType):
    full_name = graphene.String()


    def resolve_full_name(root, info):
        return f"{root['fname']} {root['lname']}"


class Query(graphene.ObjectType):
    ps = graphene.Field(Person)

    
    @staticmethod
    def resolve_ps(root, info):

        return root

schema = graphene.Schema(query=Query)
result = schema.execute("""
                    {
                        ps {
                                fullName
                        }
                    }
                        """, root={"fname":"jack", "lname":"jackson"})


print(result)
