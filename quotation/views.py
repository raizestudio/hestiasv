from rest_framework import status, viewsets
from rest_framework.response import Response

from quotation.models import Quotation, QuotationReference
from quotation.serializers import QuotationReferenceSerializer, QuotationSerializer


class QuotationReferenceViewSet(viewsets.ModelViewSet):
    queryset = QuotationReference.objects.all()
    serializer_class = QuotationReferenceSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
