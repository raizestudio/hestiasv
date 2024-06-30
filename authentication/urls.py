from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.views import TokenViewSet

router = DefaultRouter()
router.register("", TokenViewSet, basename="token")

urlpatterns = router.urls

urlpatterns += []
