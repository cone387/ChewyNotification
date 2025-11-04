from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from chewy_notification.models import NotificationTemplate
from chewy_notification.serializers import NotificationTemplateSerializer


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """通知模板视图集"""
    
    queryset = NotificationTemplate.objects.select_related("channel").all()
    serializer_class = NotificationTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["channel", "channel__type"]
    search_fields = ["name", "title"]
    ordering_fields = ["create_time", "update_time"]
    ordering = ["-create_time"]
