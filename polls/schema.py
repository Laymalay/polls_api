import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from polls.models import Poll, PassedPoll
from questions.schema import QuestionType, AnsweredQuestionType
from questions.models import AnsweredQuestion, Question, Choice
from users.schema import UserType


class PollType(DjangoObjectType):
    class Meta:
        model = Poll


class AnsweredQuestionInputType(graphene.InputObjectType):
    question_id = graphene.Int()
    choice_id = graphene.Int()


class PassedPollType(DjangoObjectType):
    class Meta:
        model = PassedPoll


class Query(object):
    all_passed_polls = graphene.List(
        PassedPollType, user=graphene.Int(), poll=graphene.Int())
    all_polls = graphene.List(PollType, creator=graphene.Int(),)

    poll = graphene.Field(PollType,
                          id=graphene.Int(),
                          title=graphene.String())

    passed_poll = graphene.Field(PassedPollType,
                                 id=graphene.Int(),)
    poll_passed_by_user = graphene.Field(
        PassedPollType, poll=graphene.Int())

    @login_required
    def resolve_poll_passed_by_user(self, info, **kwargs):
        poll = kwargs.get("poll")
        user = info.context.user
        if poll:
            return PassedPoll.objects.filter(user=user, poll=poll).last()
        return PassedPoll.objects.none()

    @login_required
    def resolve_all_polls(self, info, **kwargs):
        creator = kwargs.get('creator')
        if creator:
            return Poll.objects.filter(creator=creator)
        return Poll.objects.all()

    @login_required
    def resolve_poll(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Poll.objects.get(pk=id)

        if title is not None:
            return Poll.objects.get(title=title)

        return None

    @login_required
    def resolve_all_passed_polls(self, info, **kwargs):
        user = kwargs.get('user')
        if user:
            return PassedPoll.objects.filter(user=user)
        return PassedPoll.objects.all()

    @login_required
    def resolve_passed_poll(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return PassedPoll.objects.get(pk=id)

        return None


class UpdatePoll(graphene.Mutation):
    questions = graphene.List(QuestionType)
    creator = graphene.Field(UserType)
    image_path = graphene.String()
    title = graphene.String()
    description = graphene.String()
    id = graphene.String()

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        image_path = graphene.String()
        id = graphene.String()

    poll = graphene.Field(PollType)

    @login_required
    def mutate(self, info, title, description, image_path, id):
        poll = Poll.objects.get(pk=id)
        if title:
            poll.title = title
        if description:
            poll.description = description
        if image_path:
            poll.image_path = image_path
        poll.save()

        return UpdatePoll(creator=poll.creator,
                          id=poll.id,
                          image_path=poll.image_path,
                          description=poll.description,
                          title=poll.title)


class CreatePoll(graphene.Mutation):
    creator = graphene.Field(UserType)
    title = graphene.String(required=True)
    description = graphene.String()
    image_path = graphene.String()
    id = graphene.ID()

    class Arguments:
        title = graphene.String(required=True)
        image_path = graphene.String()
        description = graphene.String()

    poll = graphene.Field(PollType)

    @login_required
    def mutate(self, info, title, description, image_path):
        poll = Poll(title=title, creator=info.context.user,
                    description=description, image_path=image_path)
        poll.save()
        return CreatePoll(creator=poll.creator,
                          id=poll.id,
                          description=poll.description,
                          image_path=poll.image_path,
                          title=poll.title)


def create_answered_questions(input_data, passed_poll):
    correct_answers = 0

    for obj in input_data:
        question = Question.objects.get(
            pk=obj.question_id)
        choice = Choice.objects.get(pk=obj.choice_id)
        correct = question.answer == choice.title
        answered_question = AnsweredQuestion(question=question, passed_poll=passed_poll,
                                             choice=choice, correct=correct)
        answered_question.save()

        if correct:
            correct_answers += 1

    return correct_answers/len(input_data)


class CreatePassedPoll(graphene.Mutation):
    user = graphene.Field(UserType)
    poll = graphene.Field(PollType)
    score = graphene.Float()
    id = graphene.ID()

    class Arguments:
        answered_questions = graphene.List(AnsweredQuestionInputType)
        poll_id = graphene.Int()

    passed_poll = graphene.Field(PassedPollType)

    @login_required
    def mutate(self, info, poll_id, answered_questions):
        poll = Poll.objects.get(pk=poll_id)
        passed_poll = PassedPoll(poll=poll, user=info.context.user)
        passed_poll.save()
        score = create_answered_questions(answered_questions, passed_poll)
        passed_poll.score = round(score, 2)
        passed_poll.save()
        return CreatePassedPoll(user=passed_poll.user,
                                poll=passed_poll.poll,
                                score=passed_poll.score,
                                id=passed_poll.id)


class DeletePoll(graphene.Mutation):
    id = graphene.ID()

    class Arguments:
        id = graphene.ID()

    @login_required
    def mutate(self, info, id):
        poll = Poll.objects.filter(pk=id).delete()
        return DeletePoll(id=id)


class Mutation(graphene.ObjectType):
    update_poll = UpdatePoll.Field()
    create_poll = CreatePoll.Field()
    create_passed_poll = CreatePassedPoll.Field()
    delete_poll = DeletePoll.Field()
