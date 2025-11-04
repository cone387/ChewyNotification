import requests
import logging
from .base_service import BaseNotificationService

logger = logging.getLogger(__name__)


class FeishuService(BaseNotificationService):
    """飞书通知服务"""
    
    def __init__(self, config):
        super().__init__(config)
        self.webhook_url = config.get("webhook_url")
    
    def _send_implementation(self, payload):
        """
        飞书的具体发送实现
        
        飞书支持部分 Bark 参数：
        - title: 标题
        - content/body: 内容
        - url: 点击跳转（可添加按钮）
        
        Args:
            payload: 参数字典
            
        Returns:
            dict: 发送结果
        """
        url = payload.get("target") or self.webhook_url
        
        if not url:
            raise ValueError("缺少飞书Webhook URL")
        
        # 构建消息体
        card_elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": payload["content"]
                }
            }
        ]
        
        # 如果有 URL，添加按钮
        if "url" in payload:
            card_elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "🔗 点击查看"
                        },
                        "type": "default",
                        "url": payload["url"]
                    }
                ]
            })
        
        feishu_payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": payload["title"]
                    }
                },
                "elements": card_elements
            }
        }
        
        try:
            response = requests.post(url, json=feishu_payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 0:
                return {
                    "success": True,
                    "response": result
                }
            else:
                raise Exception(f"飞书返回错误: {result.get('msg')}")
        
        except requests.RequestException as e:
            raise Exception(f"飞书发送失败: {str(e)}")
