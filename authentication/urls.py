from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.views import SessionViewSet, TokenViewSet

router = DefaultRouter()
router.register("tokens", TokenViewSet, basename="token")
router.register("sessions", SessionViewSet, basename="session")

urlpatterns = router.urls

urlpatterns += []
