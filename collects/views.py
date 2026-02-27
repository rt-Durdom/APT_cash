from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .permissions import IsAuthorOrReadOnly


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Collect.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'], url_path='donors')
    def list_donors(self, request, pk=None):
        collect = get_object_or_404(Collect, pk=pk)
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


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Payment.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)
