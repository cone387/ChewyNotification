from django.apps import AppConfig


class ChewyNotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chewy_notification'
    verbose_name = '通知系统'

    def ready(self):
        """应用启动时加载信号和任务"""
        pass
