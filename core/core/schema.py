import graphene



class Query(graphene.ObjectType):
    hello = graphene.String(default_value="hello world")



schema = graphene.Schema(query=Query)
