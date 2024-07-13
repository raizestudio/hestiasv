from django.urls import path
from rest_framework.routers import DefaultRouter

from quotation.views import QuotationReferenceViewSet, QuotationViewSet

router = DefaultRouter()
router.register("references", QuotationReferenceViewSet, basename="quotation_reference")
router.register("", QuotationViewSet, basename="quotation")

urlpatterns = router.urls

urlpatterns += []
