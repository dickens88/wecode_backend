from datetime import datetime
from models.database import db

class EventArtifact(db.Model):
    __tablename__ = 't_event_artifacts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('t_event_activities.id'), nullable=False, comment='关联的AI任务ID')
    artifact_data = db.Column(db.JSON, nullable=False, comment='AI任务返回结果')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def __init__(self, activity_id, artifact_data):
        self.activity_id = activity_id
        self.artifact_data = artifact_data
    
    def to_dict(self):
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'artifact_data': self.artifact_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<EventArtifact {self.id}>'
