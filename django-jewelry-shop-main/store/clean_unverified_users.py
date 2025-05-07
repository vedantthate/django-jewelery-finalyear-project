from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete users who did not verify OTP within 10 minutes of registration'

    def handle(self, *args, **kwargs):
        threshold_time = timezone.now() - timedelta(minutes=10)
        unverified_users = User.objects.filter(is_active=False, date_joined__lt=threshold_time)
        
        count = unverified_users.count()
        unverified_users.delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {count} unverified user(s) who did not complete OTP verification.'))
