from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils.logging_config import get_logger

logger = get_logger(__name__)

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.ai_task_service = None  # 延迟初始化
    
    def _init_services(self):
        """初始化服务，在应用上下文中调用"""
        if self.ai_task_service is None:
            from services.ai_task_service import AITaskService
            self.ai_task_service = AITaskService()
    
    def start(self):
        """
        启动定时任务调度器
        """
        try:
            # 添加定时任务，每10秒执行一次
            self.scheduler.add_job(
                func=self.process_pending_tasks,
                trigger=IntervalTrigger(seconds=10),
                id='process_ai_tasks',
                name='处理待执行的AI任务',
                replace_existing=True
            )
            
            # 启动调度器
            self.scheduler.start()
            logger.info("定时任务调度器启动成功")
            
        except Exception as e:
            logger.error(f"启动定时任务调度器失败: {str(e)}")
    
    def stop(self):
        """
        停止定时任务调度器
        """
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("定时任务调度器已停止")
        except Exception as e:
            logger.error(f"停止定时任务调度器失败: {str(e)}")
    
    def process_pending_tasks(self):
        """
        处理待执行的AI任务
        """
        try:
            # 确保服务已初始化
            self._init_services()
            
            if self.ai_task_service:
                logger.debug("开始执行定时任务：处理待执行的AI任务")
                self.ai_task_service.process_pending_tasks()
            else:
                logger.warning("AI任务服务未初始化，跳过定时任务执行")
        except Exception as e:
            logger.error(f"执行定时任务异常: {str(e)}")

# 全局调度器实例
task_scheduler = TaskScheduler()
