#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI任务服务
"""

import uuid
from datetime import datetime
from models.database import db
from models.event_activity import EventActivity
from models.event_artifact import EventArtifact
from models.ai_agent_task import AIAgentTaskAsync
from services.ticket_service import TicketService
from utils.logging_config import get_logger

logger = get_logger(__name__)

class AITaskService:
    def __init__(self):
        self.ticket_service = TicketService()
    
    def create_ai_task(self, event_id, app_id, task_content):
        """
        创建AI任务
        
        Args:
            event_id: 工单ID
            app_id: 应用ID
            task_content: 任务内容
            
        Returns:
            dict: 创建的任务信息
        """
        try:
            # 生成任务ID
            task_id = str(uuid.uuid4())
            
            # 创建EventActivity记录
            event_activity = EventActivity(
                event_id=event_id,
                task_id=task_id,
                app_id=app_id,
                task_content=task_content,
                status='init'
            )
            
            # 创建AIAgentTaskAsync记录
            ai_agent_task = AIAgentTaskAsync(
                task_id=task_id,
                app_id=app_id,
                task_content=task_content,
                status='init'
            )
            
            # 保存到数据库
            db.session.add(event_activity)
            db.session.add(ai_agent_task)
            db.session.commit()
            
            logger.info(f"AI任务创建成功，task_id: {task_id}")
            
            # 返回EventActivity记录
            return event_activity.to_dict()
            
        except Exception as e:
            logger.error(f"创建AI任务失败: {str(e)}")
            db.session.rollback()
            return None
    
    def get_activities_by_event_id(self, event_id):
        """
        根据工单ID获取AI任务列表
        
        Args:
            event_id: 工单ID
            
        Returns:
            list: AI任务列表
        """
        try:
            activities = EventActivity.query.filter_by(event_id=event_id).order_by(EventActivity.created_at.desc()).all()
            return [activity.to_dict() for activity in activities]
        except Exception as e:
            logger.error(f"获取AI任务列表失败: {str(e)}")
            return []
    
    def get_artifacts_by_event_id(self, event_id):
        """
        根据工单ID获取AI任务结果列表
        
        Args:
            event_id: 工单ID
            
        Returns:
            list: AI任务结果列表
        """
        try:
            # 先获取该工单的所有活动ID
            activities = EventActivity.query.filter_by(event_id=event_id).all()
            activity_ids = [activity.id for activity in activities]
            
            if not activity_ids:
                return []
            
            # 获取对应的结果
            artifacts = EventArtifact.query.filter(EventArtifact.activity_id.in_(activity_ids)).all()
            return [artifact.to_dict() for artifact in artifacts]
        except Exception as e:
            logger.error(f"获取AI任务结果列表失败: {str(e)}")
            return []
    
    def process_pending_tasks(self):
        """
        处理待执行的AI任务（定时任务）
        """
        try:
            # 查询状态为init的AI代理任务
            pending_tasks = AIAgentTaskAsync.query.filter_by(status='init').all()
            
            if not pending_tasks:
                logger.debug("没有待执行的AI任务")
                return
            
            logger.info(f"找到 {len(pending_tasks)} 个待执行的AI任务")
            
            for task in pending_tasks:
                try:
                    # 更新状态为running
                    task.status = 'running'
                    task.updated_at = datetime.utcnow()
                    db.session.commit()
                    
                    # 调用第三方API
                    logger.info(f"开始处理任务 {task.task_id}")
                    api_result = self.ticket_service.call_ai_api(task.task_content)
                    
                    if api_result:
                        # 更新任务状态为complete，并保存结果
                        task.status = 'complete'
                        task.result = str(api_result)
                        task.updated_at = datetime.utcnow()
                        
                        # 同时更新EventActivity表
                        event_activity = EventActivity.query.filter_by(task_id=task.task_id).first()
                        if event_activity:
                            event_activity.status = 'complete'
                            event_activity.title = api_result.get('title', '')
                            event_activity.description = api_result.get('description', '')
                            event_activity.result = api_result.get('result', '')
                            event_activity.updated_at = datetime.utcnow()
                        
                        # 保存到EventArtifacts表
                        if event_activity:
                            artifact = EventArtifact(
                                activity_id=event_activity.id,
                                artifact_data=api_result
                            )
                            db.session.add(artifact)
                        
                        db.session.commit()
                        logger.info(f"任务 {task.task_id} 处理完成")
                    else:
                        # API调用失败，重置状态为init
                        task.status = 'init'
                        task.updated_at = datetime.utcnow()
                        db.session.commit()
                        logger.warning(f"任务 {task.task_id} API调用失败，重置状态")
                        
                except Exception as e:
                    logger.error(f"处理任务 {task.task_id} 异常: {str(e)}")
                    # 重置状态为init
                    task.status = 'init'
                    task.updated_at = datetime.utcnow()
                    db.session.commit()
                    
        except Exception as e:
            logger.error(f"批量处理AI任务异常: {str(e)}")
            db.session.rollback()
