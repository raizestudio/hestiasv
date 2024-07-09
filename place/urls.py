from django.urls import path
from rest_framework.routers import DefaultRouter

from place.views import PlaceViewSet

router = DefaultRouter()
router.register("", PlaceViewSet, basename="place")

urlpatterns = router.urls

urlpatterns += []
