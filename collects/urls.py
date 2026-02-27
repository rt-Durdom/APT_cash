from rest_framework.routers import DefaultRouter

from collects.views import CollectViewSet, PaymentViewSet


router = DefaultRouter()
router.register(r'collects', CollectViewSet, basename='collect')
router.register(r'payments', PaymentViewSet, basename='payment')
urlpatterns = router.urls
