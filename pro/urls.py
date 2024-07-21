from django.urls import path
from rest_framework.routers import DefaultRouter

from pro.views import EnterpriseMemberViewSet, EnterpriseViewSet, SelfEmployedViewSet

router = DefaultRouter()
router.register("enterprises", EnterpriseViewSet, basename="enterprises")
router.register("enterprise-members", EnterpriseMemberViewSet, basename="enterprise_members")
router.register("self-employed", SelfEmployedViewSet, basename="self_employed")

urlpatterns = router.urls

urlpatterns += []
