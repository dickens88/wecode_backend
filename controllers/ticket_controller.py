from flask import request, jsonify
from utils.logging_config import get_logger

logger = get_logger(__name__)

class TicketController:
    def __init__(self):
        self.ticket_service = None
        self.ai_task_service = None
    
    def _init_services(self):
        """延迟初始化服务"""
        if self.ticket_service is None:
            from services.ticket_service import TicketService
            self.ticket_service = TicketService()
        
        if self.ai_task_service is None:
            from services.ai_task_service import AITaskService
            self.ai_task_service = AITaskService()
    
    def get_tickets(self):
        """
        GET /tickets/events?offset=1&size=10&status=open&time=24h&keyword=xx
        从第三方接口获取工单数据
        """
        try:
            self._init_services()
            
            # 获取查询参数
            offset = request.args.get('offset', 1, type=int)
            size = request.args.get('size', 10, type=int)
            status = request.args.get('status')
            time = request.args.get('time')
            keyword = request.args.get('keyword')
            
            # 调用服务获取工单数据
            result = self.ticket_service.get_tickets(offset, size, status, time, keyword)
            
            if result is not None:
                return jsonify({
                    'success': True,
                    'data': result,
                    'message': '获取工单列表成功'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': '获取工单列表失败'
                }), 500
                
        except Exception as e:
            logger.error(f"获取工单列表异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'服务器内部错误: {str(e)}'
            }), 500

    def get_ticket_detail(self, event_id):
        """
        GET /tickets/events/<id>
        从第三方接口获取工单详情
        """
        try:
            self._init_services()
            
            # 调用服务获取工单详情
            result = self.ticket_service.get_ticket_detail(event_id)
            
            if result is not None:
                return jsonify({
                    'success': True,
                    'data': result,
                    'message': '获取工单详情成功'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': '获取工单详情失败'
                }), 500
                
        except Exception as e:
            logger.error(f"获取工单详情异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'服务器内部错误: {str(e)}'
            }), 500

    def create_ai_task(self, event_id):
        """
        POST /tickets/events/<id>/activities
        创建AI任务的接口
        """
        try:
            self._init_services()
            
            # 获取请求数据
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': '请求数据不能为空'
                }), 400
            
            app_id = data.get('app_id')
            task_content = data.get('task_content')
            
            if not app_id or not task_content:
                return jsonify({
                    'success': False,
                    'message': 'app_id和task_content不能为空'
                }), 400
            
            # 调用服务创建AI任务
            result = self.ai_task_service.create_ai_task(event_id, app_id, task_content)
            
            if result:
                return jsonify({
                    'success': True,
                    'data': result,
                    'message': '创建AI任务成功'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': '创建AI任务失败'
                }), 500
                
        except Exception as e:
            logger.error(f"创建AI任务异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'服务器内部错误: {str(e)}'
            }), 500

    def get_activities(self, event_id):
        """
        GET /tickets/events/<id>/activities
        返回t_event_activities表的信息
        """
        try:
            self._init_services()
            
            # 调用服务获取AI任务列表
            result = self.ai_task_service.get_activities_by_event_id(event_id)
            
            return jsonify({
                'success': True,
                'data': result,
                'message': '获取AI任务列表成功'
            }), 200
                
        except Exception as e:
            logger.error(f"获取AI任务列表异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'服务器内部错误: {str(e)}'
            }), 500

    def get_artifacts(self, event_id):
        """
        GET /tickets/events/<id>/artifacts
        返回t_event_artifacts信息
        """
        try:
            self._init_services()
            
            # 调用服务获取AI任务结果列表
            result = self.ai_task_service.get_artifacts_by_event_id(event_id)
            
            return jsonify({
                'success': True,
                'data': result,
                'message': '获取AI任务结果列表成功'
            }), 200
                
        except Exception as e:
            logger.error(f"获取AI任务结果列表异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'服务器内部错误: {str(e)}'
            }), 500
