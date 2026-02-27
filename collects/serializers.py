from rest_framework import serializers

from .models import Collect, Payment


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = [
            'id',
            'author',
            'name_collect',
            'event',
            'description',
            'current_amount',
            'target_amount',
            'donors_count',
            'image',
            'ends_collect',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'author',
            'current_amount',
            'donors_count',
            'created_at',
            'updated_at',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'collect',
            'donor',
            'amount',
            'created_at',
        ]
        read_only_fields = [
            'donor',
            'created_at',
        ]
