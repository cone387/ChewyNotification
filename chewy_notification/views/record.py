from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from chewy_notification.models import NotificationRecord
from chewy_notification.serializers import NotificationRecordSerializer


class NotificationRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """通知记录视图集（只读）"""
    
    queryset = NotificationRecord.objects.select_related(
        "template", "channel", "target"
    ).all()
    serializer_class = NotificationRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "channel", "template", "target"]
    search_fields = ["error_message"]
    ordering_fields = ["create_time", "send_time"]
    ordering = ["-create_time"]
