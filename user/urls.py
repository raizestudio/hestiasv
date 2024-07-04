from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = router.urls

urlpatterns += []
