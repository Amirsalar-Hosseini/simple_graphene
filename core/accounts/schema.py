import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django.contrib.auth.models import User
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User




class AccountsQuery(ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())


    def resolve_user(parent, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("you are gay")
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(id=id)
        return None


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()



class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)



    ok = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    def mutate(parent, info, input=None):
        user_instance = User.objects.create_user(input.username, input.email, input.password)
        ok = True
        return CreateUser(user=user_instance, ok=ok)



class Mutate(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
