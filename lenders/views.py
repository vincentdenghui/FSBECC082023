from lenders.models import Lender
from lenders.serializers import LenderSerializer
from rest_framework import viewsets, permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from lenders.renderers import CSVRenderer

class LenderViewSet(viewsets.ModelViewSet):
    queryset = Lender.objects.all()
    serializer_class = LenderSerializer
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (CSVRenderer,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['active','code']
    ordering_fields = ['created', 'code', 'upfront_commission_rate', 'trial_commission_rate','active']

    lookup_field = 'code'