# 📁 Chewy Notification 项目结构说明

## 🌳 完整目录树

```
chewy_notification/
├── __init__.py                 # 包初始化，定义版本号
├── admin.py                    # Django Admin 管理界面配置
├── apps.py                     # App 配置
├── urls.py                     # URL 路由配置
├── tasks.py                    # Celery 异步任务
├── utils.py                    # 工具函数
├── migrations/                 # 数据库迁移文件
│   └── __init__.py
├── models/                     # 数据模型层（分模块）
│   ├── __init__.py            # 导出所有模型
│   ├── base.py                # 基础模型（BaseModel）
│   ├── channel.py             # 通知渠道模型
│   ├── template.py            # 通知模板模型
│   ├── target.py              # 通知目标模型
│   └── record.py              # 通知记录模型
├── serializers/                # 序列化器层（DRF）
│   ├── __init__.py            # 导出所有序列化器
│   ├── channel.py             # 渠道序列化器
│   ├── template.py            # 模板序列化器
│   ├── target.py              # 目标序列化器
│   └── record.py              # 记录序列化器
├── views/                      # 视图层（ViewSet + APIView）
│   ├── __init__.py            # 导出所有视图
│   ├── channel.py             # 渠道视图集
│   ├── template.py            # 模板视图集
│   ├── target.py              # 目标视图集
│   ├── record.py              # 记录视图集（只读）
│   └── send.py                # 发送通知视图
├── services/                   # 服务层（业务逻辑）
│   ├── __init__.py            # 服务工厂函数
│   ├── bark_service.py        # Bark 通知服务
│   ├── ntfy_service.py        # Ntfy 通知服务
│   ├── email_service.py       # 邮件通知服务
│   └── feishu_service.py      # 飞书通知服务
└── tests/                      # 测试模块
    ├── __init__.py
    └── test_notifications.py  # 单元测试
```

## 📦 核心模块说明

### 1️⃣ Models 层（数据模型）

#### `models/base.py`
- **BaseModel**: 抽象基类，提供 `create_time` 和 `update_time` 字段
- 所有模型继承此类，统一时间戳管理

#### `models/channel.py`
- **NotificationChannel**: 通知渠道模型
- 字段：
  - `name`: 渠道名称
  - `type`: 渠道类型（bark/ntfy/email/feishu）
  - `config`: JSON 配置
  - `enabled`: 是否启用
- 表名：`chewy_notify_channel`

#### `models/template.py`
- **NotificationTemplate**: 通知模板模型
- 字段：
  - `name`: 模板名称（唯一）
  - `title`: 标题模板
  - `content`: 内容模板
  - `channel`: 外键关联渠道
- 表名：`chewy_notify_template`
- 支持 `{{variable}}` 语法变量替换

#### `models/target.py`
- **NotificationTarget**: 通知目标模型
- 字段：
  - `alias`: 目标别名
  - `target_type`: 目标类型
  - `target_value`: 目标值（邮箱、token等）
- 表名：`chewy_notify_target`
- 唯一约束：`(target_type, target_value)`

#### `models/record.py`
- **NotificationRecord**: 通知发送记录
- 字段：
  - `template`: 使用的模板
  - `channel`: 发送渠道
  - `target`: 接收目标
  - `status`: 发送状态（pending/success/failed/retry）
  - `response`: 响应数据
  - `send_time`: 发送时间
  - `error_message`: 错误信息
- 表名：`chewy_notify_record`

---

### 2️⃣ Serializers 层（序列化）

各序列化器对应相应的模型，提供：
- 数据验证
- JSON 序列化/反序列化
- 关联字段展示（如 `channel_name`）
- 自定义验证逻辑

#### 特点：
- `channel.py`: 验证渠道配置完整性
- `template.py`: 验证渠道是否启用
- `target.py`: 验证邮箱格式、Webhook URL 格式
- `record.py`: 只读序列化器，展示关联信息

---

### 3️⃣ Views 层（API 接口）

#### ViewSet（标准 CRUD）
- **NotificationChannelViewSet**: 渠道管理
- **NotificationTemplateViewSet**: 模板管理
- **NotificationTargetViewSet**: 目标管理
- **NotificationRecordViewSet**: 记录查询（只读）

#### 功能：
- 分页、搜索、过滤、排序
- 使用 `DjangoFilterBackend` 和 `SearchFilter`

#### APIView（自定义接口）
- **NotificationSendView**: 手动发送通知
  - 支持同步/异步发送
  - 模板变量渲染
  - 错误处理和状态更新

---

### 4️⃣ Services 层（核心业务）

#### 作用
封装各渠道的发送逻辑，统一接口规范

#### `bark_service.py`
- **BarkService**: Bark iOS 推送
- 配置：`server_url`
- 方法：`send(device_key, title, content)`

#### `ntfy_service.py`
- **NtfyService**: Ntfy 推送
- 配置：`server_url`, `token`（可选）
- 方法：`send(topic, title, content)`

#### `email_service.py`
- **EmailService**: 邮件发送
- 配置：`host`, `port`, `username`, `password`, `from_email`, `use_tls`
- 方法：`send(to_email, title, content)`
- 使用 Django 内置邮件系统

#### `feishu_service.py`
- **FeishuService**: 飞书机器人
- 配置：`webhook_url`
- 方法：`send(webhook_url, title, content)`
- 发送交互式卡片消息

#### `services/__init__.py`
- **get_service_for_channel()**: 服务工厂函数
- 根据渠道类型返回对应服务实例

---

### 5️⃣ Tasks 层（异步任务）

#### `tasks.py`
- **send_notification_task**: Celery 异步任务
- 功能：
  - 从数据库获取记录
  - 渲染模板
  - 调用服务发送
  - 更新记录状态
- 兼容设计：无 Celery 时降级为普通函数

---

### 6️⃣ Utils 层（工具函数）

#### `utils.py`
- **render_notification_content()**: 模板渲染
- **validate_channel_config()**: 配置验证
- **format_notification_record()**: 记录格式化

---

### 7️⃣ Admin 层（管理界面）

#### `admin.py`
提供 Django Admin 界面：
- **NotificationChannelAdmin**: 渠道管理
- **NotificationTemplateAdmin**: 模板管理
- **NotificationTargetAdmin**: 目标管理
- **NotificationRecordAdmin**: 记录查看（只读）

特性：
- 字段分组展示
- 搜索和过滤
- 时间字段折叠
- 自定义列表显示

---

### 8️⃣ URLs 层（路由配置）

#### `urls.py`
- 使用 `DefaultRouter` 自动生成 RESTful 路由
- 注册所有 ViewSet
- 添加自定义发送接口

#### API 端点：
```
/api/notifications/channels/          # 渠道列表
/api/notifications/channels/{id}/     # 渠道详情
/api/notifications/templates/         # 模板列表
/api/notifications/templates/{id}/    # 模板详情
/api/notifications/targets/           # 目标列表
/api/notifications/targets/{id}/      # 目标详情
/api/notifications/records/           # 记录列表
/api/notifications/send/              # 发送接口
```

---

### 9️⃣ Tests 层（测试）

#### `tests/test_notifications.py`
完整的单元测试覆盖：
- 模型创建测试
- 模板渲染测试
- 唯一性约束测试
- 状态更新测试
- 服务获取测试
- 工具函数测试

---

## 🔄 架构分层

```
┌─────────────────┐
│   View Layer    │  ← API 接口、请求处理
├─────────────────┤
│ Serializer Layer│  ← 数据验证、序列化
├─────────────────┤
│  Service Layer  │  ← 业务逻辑、渠道发送
├─────────────────┤
│   Model Layer   │  ← 数据模型、ORM
└─────────────────┘
        ↕
┌─────────────────┐
│   Task Layer    │  ← 异步任务（Celery）
└─────────────────┘
```

## 🎯 设计模式

### 1. 工厂模式
- `get_service_for_channel()` 根据渠道类型创建服务实例

### 2. 策略模式
- 每个 Service 类实现统一的 `send()` 接口
- 不同渠道有不同的发送策略

### 3. 模板方法模式
- `BaseModel` 定义通用字段
- 子模型扩展特定字段

### 4. 单一职责原则
- Models：数据定义
- Serializers：数据验证
- Views：请求处理
- Services：业务逻辑

## 🛠️ 技术栈

- **Django**: Web 框架
- **Django REST Framework**: API 框架
- **django-filter**: 过滤器
- **Celery**: 异步任务（可选）
- **requests**: HTTP 请求

## 📊 数据流程

### 发送通知流程：
```
1. API 请求 (views/send.py)
   ↓
2. 验证参数、获取模板和目标
   ↓
3. 创建通知记录 (models/record.py)
   ↓
4. 渲染模板内容
   ↓
5. 获取服务实例 (services/)
   ↓
6. 调用服务发送
   ↓
7. 更新记录状态
   ↓
8. 返回结果
```

## ✅ 最佳实践

1. **分层清晰**: 每层职责明确
2. **可测试性**: 提供完整单元测试
3. **可扩展性**: 新增渠道只需添加 Service
4. **错误处理**: 完整的异常捕获和记录
5. **日志记录**: 关键操作记录日志
6. **配置验证**: 严格的数据验证
7. **数据库优化**: 使用索引、select_related
8. **API 规范**: 遵循 RESTful 设计

## 📝 命名规范

- 模型：`NotificationXxx`
- 表名：`chewy_notify_xxx`
- 序列化器：`XxxSerializer`
- 视图：`XxxViewSet` / `XxxView`
- 服务：`XxxService`
- 任务：`xxx_task`

## 🚀 扩展建议

1. 添加更多通知渠道（微信、钉钉等）
2. 实现消息队列优先级
3. 添加发送频率限制
4. 实现消息模板变量类型验证
5. 添加消息发送统计和分析
6. 实现批量发送功能
7. 添加消息撤回功能
8. 实现消息发送重试机制
