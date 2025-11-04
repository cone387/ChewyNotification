# Chewy Notification 集成指南

## 📦 安装步骤

### 1. 安装依赖

```bash
pip install django djangorestframework django-filter requests
# 可选：异步任务支持
pip install celery redis
```

### 2. 在 Django 项目中注册 App

编辑 `settings.py`：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'django_filters',
    
    # Chewy Notification
    'chewy_notification',
]

# REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
```

### 3. 配置 URL

编辑主项目的 `urls.py`：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chewy_notification.urls')),
]
```

### 4. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户（访问 Admin）

```bash
python manage.py createsuperuser
```

## 🔧 Celery 配置（可选）

如果需要异步发送通知，配置 Celery：

**celery.py**：

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**settings.py**：

```python
# Celery 配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
```

启动 Celery Worker：

```bash
celery -A your_project worker -l info
```

## 📡 API 使用示例

### 1. 创建通知渠道

```bash
POST /api/notifications/channels/
{
  "name": "我的Bark渠道",
  "type": "bark",
  "config": {
    "server_url": "https://api.day.app"
  },
  "enabled": true
}
```

### 2. 创建通知模板

```bash
POST /api/notifications/templates/
{
  "name": "欢迎模板",
  "title": "欢迎 {{username}}",
  "content": "你好，{{username}}！欢迎使用我们的系统。",
  "channel": 1
}
```

### 3. 创建通知目标

```bash
POST /api/notifications/targets/
{
  "alias": "我的设备",
  "target_type": "bark_token",
  "target_value": "your_bark_token_here"
}
```

### 4. 发送通知

```bash
POST /api/notifications/send/
{
  "template_id": 1,
  "target_id": 1,
  "context": {
    "username": "张三"
  },
  "async_send": false
}
```

### 5. 查询发送记录

```bash
GET /api/notifications/records/
GET /api/notifications/records/?status=success
GET /api/notifications/records/?channel=1
```

## 🔌 渠道配置说明

### Bark

```json
{
  "server_url": "https://api.day.app"
}
```

### Ntfy

```json
{
  "server_url": "https://ntfy.sh",
  "token": "optional_auth_token"
}
```

### Email

```json
{
  "host": "smtp.gmail.com",
  "port": 587,
  "username": "your_email@gmail.com",
  "password": "your_password",
  "from_email": "your_email@gmail.com",
  "use_tls": true
}
```

### 飞书

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
}
```

## 🎯 使用场景示例

### 场景1：用户注册通知

```python
from chewy_notification.models import NotificationTemplate, NotificationTarget, NotificationRecord
from chewy_notification.tasks import send_notification_task

# 获取模板和目标
template = NotificationTemplate.objects.get(name="用户注册")
target = NotificationTarget.objects.get(alias="管理员邮箱")

# 创建记录
record = NotificationRecord.objects.create(
    template=template,
    channel=template.channel,
    target=target,
    status="pending"
)

# 异步发送
context = {"username": "新用户", "email": "newuser@example.com"}
send_notification_task.delay(record.id, context)
```

### 场景2：系统监控告警

```python
from chewy_notification.views.send import NotificationSendView

# 直接调用发送接口
data = {
    "template_id": 5,  # 告警模板
    "target_id": 2,    # 运维人员
    "context": {
        "service": "数据库",
        "status": "CPU使用率90%"
    },
    "async_send": True
}
# 通过 API 发送或在代码中调用
```

## 📊 数据库表结构

- `chewy_notify_channel` - 通知渠道
- `chewy_notify_template` - 通知模板
- `chewy_notify_target` - 通知目标
- `chewy_notify_record` - 通知记录

## 🛡️ 权限与安全

建议在生产环境中：

1. 为 API 添加认证（JWT、Session 等）
2. 对敏感配置（如邮箱密码）进行加密存储
3. 限制发送频率，防止滥用
4. 记录详细日志，便于审计

## 📝 日志配置

在 `settings.py` 中配置日志：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'chewy_notification': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```
