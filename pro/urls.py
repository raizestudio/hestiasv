from django.urls import path
from rest_framework.routers import DefaultRouter

from pro.views import EnterpriseViewSet, SelfEmployedViewSet

router = DefaultRouter()
router.register("enterprises", EnterpriseViewSet, basename="enterprise")
router.register("self-employed", SelfEmployedViewSet, basename="self_employed")

urlpatterns = router.urls

urlpatterns += []
