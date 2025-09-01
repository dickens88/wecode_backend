from flask import Flask, request, jsonify
from utils.config import Config
from utils.logging_config import setup_app_logging
from models.database import db
from controllers.ticket_controller import TicketController
from scheduler import task_scheduler
import logging

def create_app():
    """
    创建Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    config = Config()
    app.config.from_object(config)
    
    # 设置日志系统
    app_logger = setup_app_logging(
        app_name='WeCodeSecTools',
        log_dir=config.LOG_DIR
    )
    
    # 初始化数据库
    db.init_app(app)
    
    # 创建控制器实例
    ticket_controller = TicketController()
    
    # 注册API路由 - 使用add_resource方式集中管理
    _register_api_routes(app, ticket_controller)
    
    # 创建数据库表
    with app.app_context():
        try:
            db.create_all()
            app_logger.info("数据库表创建成功")
        except Exception as e:
            app_logger.error(f"数据库表创建失败: {str(e)}")
    
    return app

def _register_api_routes(app, ticket_controller):
    """
    注册所有API路由
    """
    
    # 工单相关API
    @app.route('/tickets/events', methods=['GET'])
    def get_tickets():
        """获取工单列表"""
        return ticket_controller.get_tickets()
    
    @app.route('/tickets/events/<event_id>', methods=['GET'])
    def get_ticket_detail(event_id):
        """获取工单详情"""
        return ticket_controller.get_ticket_detail(event_id)
    
    @app.route('/tickets/events/<event_id>/activities', methods=['POST'])
    def create_ai_task(event_id):
        """创建AI任务"""
        return ticket_controller.create_ai_task(event_id)
    
    @app.route('/tickets/events/<event_id>/activities', methods=['GET'])
    def get_activities(event_id):
        """获取AI任务列表"""
        return ticket_controller.get_activities(event_id)
    
    @app.route('/tickets/events/<event_id>/artifacts', methods=['GET'])
    def get_artifacts(event_id):
        """获取AI任务结果"""
        return ticket_controller.get_artifacts(event_id)
    
    # 健康检查接口
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查接口"""
        return jsonify({
            'success': True,
            'message': '服务运行正常',
            'status': 'healthy'
        }), 200
    
    # 根路径
    @app.route('/', methods=['GET'])
    def index():
        """根路径"""
        return jsonify({
            'success': True,
            'message': 'WeCodeSecTools API Server',
            'version': '1.0.0',
            'endpoints': {
                'tickets': '/tickets/events',
                'health': '/health'
            }
        }), 200

def main():
    """
    主函数
    """
    app = create_app()
    
    # 启动定时任务调度器
    task_scheduler.start()
    
    try:
        # 启动Flask应用
        app.run(
            host=app.config['FLASK_HOST'],
            port=app.config['FLASK_PORT'],
            debug=app.config['FLASK_DEBUG']
        )
    except KeyboardInterrupt:
        print("\n正在关闭应用...")
        task_scheduler.stop()
    except Exception as e:
        print(f"应用启动失败: {str(e)}")
        task_scheduler.stop()

if __name__ == '__main__':
    main()
