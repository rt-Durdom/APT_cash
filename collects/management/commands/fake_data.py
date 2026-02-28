import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Count, Sum
from faker import Faker

from collects.models import Collect, Payment, EVENT_CHOICES

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = []
        for i in range(50):
            user_ = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='12345678',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            users.append(user_)

        event_list = [c[0] for c in EVENT_CHOICES]
        collects = []
        for i in range(1000):
            coll = Collect.objects.create(
                author=random.choice(users),
                name_collect=fake.sentence(nb_words=5),
                event=random.choice(event_list),
                description=fake.text(max_nb_chars=200),
                target_amount=Decimal(random.randint(1000, 200000)),
                current_amount=Decimal('0'),
                donors_count=0,
            )
            collects.append(coll)

        for i in range(5000):
            Payment.objects.create(
                collect=random.choice(collects),
                donor=random.choice(users),
                amount=Decimal(random.randint(10, 5000)),
            )

        for collect in Collect.objects.all():
            data = Payment.objects.filter(collect=collect).aggregate(
                total=Sum('amount'),
                num=Count('id'),
            )
            collect.current_amount = data['total'] or 0
            collect.donors_count = data['num'] or 0
            collect.save()
        print('Готово.')
