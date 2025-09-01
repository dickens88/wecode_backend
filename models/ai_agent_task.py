#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI代理任务异步表模型
"""

from datetime import datetime
from models.database import db

class AIAgentTaskAsync(db.Model):
    """AI代理任务异步表"""
    __tablename__ = 't_ai_agent_task_async'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增主键')
    task_id = db.Column(db.String(36), unique=True, nullable=False, comment='任务UUID')
    app_id = db.Column(db.String(100), nullable=False, comment='应用ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    task_content = db.Column(db.Text, nullable=False, comment='任务内容')
    status = db.Column(db.String(20), default='init', comment='任务状态: init, running, complete')
    result = db.Column(db.Text, comment='任务结果（由AI返回结果填充）')
    
    def __repr__(self):
        return f'<AIAgentTaskAsync {self.task_id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'app_id': self.app_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'task_content': self.task_content,
            'status': self.status,
            'result': self.result
        }
