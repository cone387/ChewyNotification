from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chewy_notification.views import (
    NotificationChannelViewSet,
    NotificationTemplateViewSet,
    NotificationTargetViewSet,
    NotificationRecordViewSet,
    NotificationSendView,
)

# 创建路由器
router = DefaultRouter()

# 注册 ViewSet
router.register(r"channels", NotificationChannelViewSet, basename="channel")
router.register(r"templates", NotificationTemplateViewSet, basename="template")
router.register(r"targets", NotificationTargetViewSet, basename="target")
router.register(r"records", NotificationRecordViewSet, basename="record")

# URL 配置
urlpatterns = [
    # API 路由
    path("api/notifications/", include(router.urls)),
    
    # 手动发送接口
    path("api/notifications/send/", NotificationSendView.as_view(), name="notification-send"),
]
