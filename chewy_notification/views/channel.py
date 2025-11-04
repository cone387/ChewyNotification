from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from chewy_notification.models import NotificationChannel
from chewy_notification.serializers import NotificationChannelSerializer


class NotificationChannelViewSet(viewsets.ModelViewSet):
    """通知渠道视图集"""
    
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["type", "enabled"]
    search_fields = ["name"]
    ordering_fields = ["create_time", "update_time"]
    ordering = ["-create_time"]
