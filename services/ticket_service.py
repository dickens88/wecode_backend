import requests
from flask import current_app
from utils.logging_config import get_logger

logger = get_logger(__name__)

class TicketService:
    def __init__(self):
        self.base_url = current_app.config['THIRD_PARTY_API_BASE_URL']
        self.api_key = current_app.config['THIRD_PARTY_API_KEY']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_tickets(self, offset=1, size=10, status=None, time=None, keyword=None):
        """
        从第三方API获取工单列表
        """
        try:
            params = {
                'offset': offset,
                'size': size
            }
            
            if status:
                params['status'] = status
            if time:
                params['time'] = time
            if keyword:
                params['keyword'] = keyword
            
            response = requests.get(
                f"{self.base_url}/tickets",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"获取工单列表失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"获取工单列表异常: {str(e)}")
            return None
    
    def get_ticket_detail(self, ticket_id):
        """
        从第三方API获取工单详情
        """
        try:
            response = requests.get(
                f"{self.base_url}/tickets/{ticket_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"获取工单详情失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"获取工单详情异常: {str(e)}")
            return None
    
    def call_ai_api(self, task_content):
        """
        调用AI API
        
        Args:
            task_content: 任务内容
            
        Returns:
            dict: AI API返回结果，包含title、description、result字段
        """
        try:
            # 这里应该是调用真实的AI API
            # 目前返回模拟数据
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'task_content': task_content,
                'model': 'gpt-4'  # 或其他AI模型
            }
            
            # 模拟API调用
            # response = requests.post(f"{self.base_url}/ai/process", json=data, headers=headers)
            # response.raise_for_status()
            # return response.json()
            
            # 返回模拟数据
            mock_result = {
                'title': f'AI分析结果: {task_content[:50]}...',
                'description': f'基于任务内容"{task_content}"的详细分析描述',
                'result': f'AI处理完成，任务内容: {task_content}。分析结果包括风险评估、建议措施等详细信息。'
            }
            
            logger.info(f"AI API调用成功，任务内容: {task_content[:100]}...")
            return mock_result
            
        except Exception as e:
            logger.error(f"调用AI API异常: {str(e)}")
            return None
