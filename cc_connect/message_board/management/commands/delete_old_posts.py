from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from message_board.models import Message

class Command(BaseCommand):
    help = 'Delete posts older than 14 days'

    def handle(self, *args, **kwargs):
        threshold_date = now() - timedelta(days=14)
        old_posts = Message.objects.filter(timestamp__lt=threshold_date)
        count = old_posts.count()
        old_posts.delete()
        self.stdout.write(f'{count} old posts deleted.')