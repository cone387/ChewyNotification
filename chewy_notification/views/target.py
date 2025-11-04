from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from chewy_notification.models import NotificationTarget
from chewy_notification.serializers import NotificationTargetSerializer


class NotificationTargetViewSet(viewsets.ModelViewSet):
    """通知目标视图集"""
    
    queryset = NotificationTarget.objects.all()
    serializer_class = NotificationTargetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["target_type"]
    search_fields = ["alias", "target_value"]
    ordering_fields = ["create_time", "update_time"]
    ordering = ["-create_time"]
