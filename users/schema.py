from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload

import graphene
from graphene_django import DjangoObjectType
from users.models import CustomUser
from aws.client import AwsClient


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
    avatar = graphene.String(required=False)

    id = graphene.ID()

    class Arguments:
        id = graphene.ID()
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        about = graphene.String(required=True)
        avatar = Upload(required=False)

    @login_required
    def mutate(self, info, id, email, avatar, first_name, last_name, about):
        url = None

        if avatar and not isinstance(avatar, str):
            cli = AwsClient()
            key = cli.upload_file_obj(avatar)
            url = cli.generate_presigned_url(key)
            CustomUser.objects.filter(pk=id).update(
                avatar_key=key, avatar=url)

        CustomUser.objects.filter(pk=id).update(
            email=email, first_name=first_name, last_name=last_name, about=about)

        return UpdateUser(id=id,
                          email=email,
                          avatar=url,
                          first_name=first_name,
                          last_name=last_name,
                          about=about)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    @login_required
    def resolve_users(self, info):
        return CustomUser.objects.all()

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    @login_required
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            user = CustomUser.objects.get(pk=id)
            return user

        return None
