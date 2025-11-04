# 📨 Chewy Notification

一个通用的 Django 通知系统 App，支持多渠道通知发送（Bark、Ntfy、Email、飞书）。

## ✨ 特性

- 🔌 **多渠道支持**: Bark、Ntfy、Email、飞书
- 🎯 **模板系统**: 支持变量替换的消息模板
- 📊 **完整记录**: 自动记录所有发送历史
- ⚡ **异步发送**: 可选的 Celery 异步任务支持
- 🛠️ **RESTful API**: 完整的 DRF 接口
- 🎨 **Admin 管理**: 直观的后台管理界面
- 📦 **独立安装**: 可集成到任何 Django 项目
- 🧪 **完整测试**: 提供单元测试用例

## 📦 安装

```bash
pip install django djangorestframework django-filter requests
```

将 App 添加到 Django 项目（详见 `INTEGRATION_GUIDE.md`）

## 🚀 快速开始

### 1. 注册 App

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'django_filters',
    'chewy_notification',
]
```

### 2. 配置 URL

```python
urlpatterns = [
    path('', include('chewy_notification.urls')),
]
```

### 3. 执行迁移

```bash
python manage.py migrate
```

### 4. 创建渠道和模板

通过 Admin 后台或 API 创建通知渠道和模板。

### 5. 发送通知

```python
from chewy_notification.tasks import send_notification_task

send_notification_task.delay(
    record_id=1,
    context={'username': '张三'}
)
```

## 📖 文档

- [集成指南](INTEGRATION_GUIDE.md) - 如何集成到 Django 项目
- [项目结构](PROJECT_STRUCTURE.md) - 详细的架构和代码说明
- [示例项目](example_project/) - 完整的使用示例

## 🏗️ 项目结构

```
chewy_notification/
├── models/         # 数据模型（渠道、模板、目标、记录）
├── serializers/    # DRF 序列化器
├── views/          # API 视图
├── services/       # 各渠道发送服务
├── tasks.py        # Celery 异步任务
├── admin.py        # Admin 管理
└── tests/          # 单元测试
```

## 📡 API 端点

```
GET/POST    /api/notifications/channels/      # 渠道管理
GET/POST    /api/notifications/templates/     # 模板管理
GET/POST    /api/notifications/targets/       # 目标管理
GET         /api/notifications/records/       # 发送记录
POST        /api/notifications/send/          # 手动发送
```

## 🔧 支持的渠道

| 渠道 | 类型 | 配置项 |
|------|------|--------|
| Bark | iOS 推送 | `server_url` |
| Ntfy | 跨平台推送 | `server_url`, `token` |
| Email | 邮件 | `host`, `port`, `username`, `password` |
| 飞书 | 企业通知 | `webhook_url` |

## 🧪 测试

```bash
cd example_project
python manage.py test chewy_notification
```

所有 12 个单元测试应该全部通过。

## 📊 数据库表

- `chewy_notify_channel` - 通知渠道
- `chewy_notify_template` - 通知模板
- `chewy_notify_target` - 通知目标
- `chewy_notify_record` - 发送记录

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

## 👨‍💻 作者

Chewy Notification Team