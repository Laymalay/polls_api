from django.core.management.base import BaseCommand, CommandError
from users.models import CustomUser as User
from aws.config import BUCKET_NAME
from aws.client import AwsClient


class Command(BaseCommand):
    help = 'Regenerate avatar urls from s3'

    def handle(self, *args, **options):
        cli = AwsClient()

        try:
            for user in User.objects.all():
                user.avatar = cli.generate_presigned_url(user.avatar_key)
                user.save()
        except Exception as e:
            raise CommandError(e)
