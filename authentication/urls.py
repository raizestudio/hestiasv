from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.views import SessionViewSet, TokenViewSet

router = DefaultRouter()
router.register("", TokenViewSet, basename="token")
router.register("session", SessionViewSet, basename="session")

urlpatterns = router.urls

urlpatterns += []
