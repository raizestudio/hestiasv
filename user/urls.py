from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import GroupViewSet, RoleViewSet, UserViewSet

router = DefaultRouter()
router.register("groups", GroupViewSet, basename="groups")
router.register("roles", RoleViewSet, basename="roles")
router.register("", UserViewSet, basename="user")

urlpatterns = router.urls

urlpatterns += []
