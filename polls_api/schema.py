import graphene
import graphql_jwt
from django.contrib.auth import logout

import polls.schema
import questions.schema
import users.schema
from users.schema import UserType
from graphene_django.types import DjangoObjectType


class Query(polls.schema.Query,
            questions.schema.Query,
            users.schema.Query,
            graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        if info.context.user.is_authenticated:
            logout(info.context)
        return cls(user=info.context.user)


class Mutation(polls.schema.Mutation,
               questions.schema.Mutation,
               users.schema.Mutation,
               graphene.ObjectType):

    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
