import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from questions.models import Question, Choice, AnsweredQuestion
from polls.models import Poll


class QuestionType(DjangoObjectType):
    stat = graphene.types.json.JSONString()

    class Meta:
        model = Question


class AnsweredQuestionType(DjangoObjectType):
    class Meta:
        model = AnsweredQuestion


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice


class Query(object):
    all_questions = graphene.List(QuestionType)
    all_choices = graphene.List(ChoiceType)

    question = graphene.Field(QuestionType,
                              id=graphene.Int(), stat=graphene.Boolean())

    @staticmethod
    def calculate_stat(question):
        stat = {}
        
        choices = Choice.objects.filter(question=question.id)
        for choice in choices:
            stat.update({choice.id: 0})

        answers = AnsweredQuestion.objects.filter(question=question.id)
        for answer in answers:
            stat[answer.choice.id] += 1

        return stat

    @login_required
    def resolve_all_questions(self, info, **kwargs):
        return Question.objects.all()

    @login_required
    def resolve_all_choices(self, info, **kwargs):
        return Choice.objects.all()

    @login_required
    def resolve_question(self, info, **kwargs):
        id = kwargs.get('id')
        with_stat = kwargs.get('stat')

        if id is not None:
            question = Question.objects.get(pk=id)
            if with_stat:
                question.stat = Query.calculate_stat(question)
            return question
        return None


class CreateQuestion(graphene.Mutation):
    id = graphene.ID()

    class Arguments:
        title = graphene.String(required=True)
        answer = graphene.String(required=True)
        poll_id = graphene.Int()

    question = graphene.Field(QuestionType)

    def mutate(self, info, title, poll_id, answer):
        poll = Poll.objects.get(pk=poll_id)
        question = Question(title=title, poll=poll, answer=answer)
        question.save()
        return CreateQuestion(id=question.id)


class CreateChoice(graphene.Mutation):
    title = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        question_id = graphene.Int()

    choice = graphene.Field(ChoiceType)

    def mutate(self, info, title, question_id):
        question = Question.objects.get(pk=question_id)
        choice = Choice(title=title, question=question)
        choice.save()
        return CreateChoice(title=choice.title)


class Mutation(graphene.ObjectType):
    create_choice = CreateChoice.Field()
    create_question = CreateQuestion.Field()
