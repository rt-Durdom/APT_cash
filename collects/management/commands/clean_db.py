from django.core.management.base import BaseCommand

from collects.models import Collect, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        Payment.objects.all().delete()
        Collect.objects.all().delete()
        print('Сборы и платежи удалены.')
