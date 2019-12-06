from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

import graphene
from graphene_django import DjangoObjectType
from users.models import CustomUser


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser


class CreateUser(graphene.Mutation):
    username = graphene.String(required=True)
    email = graphene.String(required=True)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(username=user.username, email=user.email)


class UpdateUser(graphene.Mutation):
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    about = graphene.String(required=True)
    id = graphene.ID()

    class Arguments:
        id = graphene.ID()
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        about = graphene.String(required=True)

    @login_required
    def mutate(self, info, id, email, first_name, last_name, about):
        CustomUser.objects.filter(pk=id).update(
            email=email, first_name=first_name, last_name=last_name, about=about)

        return UpdateUser(id=id, email=email, first_name=first_name, last_name=last_name, about=about)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
