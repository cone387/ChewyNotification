"""
URL configuration for example_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Chewy Notification API
    path('', include('chewy_notification.urls')),
]
