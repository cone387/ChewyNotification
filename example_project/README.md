# Example Project

## 快速开始

### 1. 安装依赖

```bash
pip install django djangorestframework django-filter requests
```

### 2. 执行迁移

```bash
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 启动服务

```bash
python manage.py runserver
```

### 5. 访问

- Admin: http://127.0.0.1:8000/admin/
- API Root: http://127.0.0.1:8000/api/notifications/
- API 文档: http://127.0.0.1:8000/api/notifications/channels/

## API 测试

使用 curl 或 Postman 测试接口：

```bash
# 创建渠道
curl -X POST http://127.0.0.1:8000/api/notifications/channels/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试Bark渠道",
    "type": "bark",
    "config": {"server_url": "https://api.day.app"},
    "enabled": true
  }'

# 获取渠道列表
curl http://127.0.0.1:8000/api/notifications/channels/
```
