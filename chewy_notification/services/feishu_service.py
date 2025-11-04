import requests
import logging

logger = logging.getLogger(__name__)


class FeishuService:
    """飞书通知服务"""
    
    def __init__(self, config):
        """
        初始化飞书服务
        
        配置示例:
        {
            "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
        }
        """
        self.webhook_url = config.get("webhook_url")
    
    def send(self, webhook_url, title, content):
        """
        发送飞书通知
        
        Args:
            webhook_url: 飞书 Webhook 地址（如果为空则使用配置中的）
            title: 通知标题
            content: 通知内容
        
        Returns:
            dict: 发送结果
        """
        url = webhook_url or self.webhook_url
        
        if not url:
            raise ValueError("缺少飞书Webhook URL")
        
        # 构建消息体
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": content
                        }
                    }
                ]
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"飞书通知发送成功")
                return {
                    "success": True,
                    "response": result
                }
            else:
                logger.error(f"飞书通知发送失败: {result}")
                raise Exception(f"飞书返回错误: {result.get('msg')}")
        
        except requests.RequestException as e:
            logger.error(f"飞书通知发送失败: {str(e)}")
            raise Exception(f"飞书发送失败: {str(e)}")
