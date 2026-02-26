from django.contrib import admin
from .models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_collect",
        "author",
        "event",
        "current_amount",
        "target_amount",
        "donors_count",
        "ends_collect",
        "created_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "collect",
        "donor",
        "amount",
        "created_at",
    )
