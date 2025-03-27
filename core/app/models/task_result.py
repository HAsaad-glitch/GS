from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text

class TaskResult(Model):
    id = Column(Integer, primary_key=True)
    task_id = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), default='pending')  # e.g., 'pending', 'completed', 'failed'
    result = Column(Text)  # Store the CrewAI result as text

    def __repr__(self):
        return f"<TaskResult(task_id={self.task_id}, status={self.status})>"