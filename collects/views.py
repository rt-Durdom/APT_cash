from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .permissions import IsAuthorOrReadOnly
from .emails import send_email


@method_decorator(cache_page(60 * 5), name='list')
@method_decorator(cache_page(60*15), name='retrieve')
@method_decorator(cache_page(60*15), name='list_donors')
class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Collect.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)

        send_email(
            subject='Сбор создан',
            message=(
                f'Добрый день, {self.request.user.username}!\n'
                f'Сбор "{collect.name_collect}" создан.\n'
            ),
            recipient=self.request.user.email
        )

    @action(detail=True, methods=['get'], url_path='donors')
    def list_donors(self, request, pk=None):
        collect = self.get_object()
        payments = (
            Payment.objects
            .filter(collect=collect)
            .select_related('donor')
            .order_by('-created_at')
        )
        info = [
            {
                'donor_id': payment.donor.id,
                'donor': payment.donor.username,
                'amount': payment.amount,
                'created_at': payment.created_at,
            }
            for payment in payments
        ]
        return Response(info)


@method_decorator(cache_page(60 * 5), name='list')
@method_decorator(cache_page(60*15), name='retrieve')
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Payment.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save(donor=self.request.user)
        collect = payment.collect
        collect.current_amount += payment.amount
        collect.donors_count += 1
        collect.save(update_fields=['current_amount', 'donors_count'])

        send_email(
            subject='Платеж получен',
            message=(
                f'Добрый день, {self.request.user.username}!\n'
                f'Платеж на сбор "{payment.collect.name_collect}" получен.\n'
            ),
            recipient=self.request.user.email
        )
