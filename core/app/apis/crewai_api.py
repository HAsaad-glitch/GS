from flask_appbuilder.api import BaseApi
from flask_appbuilder.api import expose
from flask import request, send_file
import threading
import json
import os
from GS.crew_ai.runners.crew_runner import run_data_analysis_crew
from uuid import uuid4
from GS.core.app import db
from GS.core.app.models.task_result import TaskResult

class CrewAIApi(BaseApi):
    resource_name = 'crewai'

    @expose('/start_task', methods=['POST'])
    def start_task(self):
        session = db.session
        """Start a CrewAI task in the background."""
        data = request.json
        task_id = str(uuid4())  # Generate a unique task ID
        # Save initial task status
        task = TaskResult(task_id=task_id, status='pending')
        session.add(task)
        session.commit()
        # Run CrewAI task in a separate thread
        thread = threading.Thread(target=run_data_analysis_crew, args=(task_id, data))
        thread.start()
        return self.response(202, task_id=task_id, message="Task started")
    
    @expose('/start_data_analysis', methods=['POST'])
    def start_data_analysis(self):
        session = db.session
        """Start a data analysis task in the background using the newer crew structure."""
        data = request.json
        task_id = str(uuid4())  # Generate a unique task ID
        # Save initial task status
        task = TaskResult(task_id=task_id, status='pending')
        session.add(task)
        session.commit()
        # Run CrewAI task in a separate thread
        thread = threading.Thread(target=run_data_analysis_crew, args=(task_id, data))
        thread.start()
        return self.response(202, task_id=task_id, message="Data analysis task started")

    @expose('/start_comprehensive_analysis', methods=['POST'])
    def start_comprehensive_analysis(self):
        # Import here to avoid circular dependency
        from GS.crew_ai.flows.data_analysis_flow import run_flow_analysis
        
        session = db.session
        """Start a comprehensive analysis flow that combines data analysis and summary."""
        data = request.json
        task_id = str(uuid4())  # Generate a unique task ID
        # Save initial task status
        task = TaskResult(task_id=task_id, status='pending')
        session.add(task)
        session.commit()
        # Run the comprehensive analysis flow in a separate thread
        thread = threading.Thread(target=run_flow_analysis, args=(task_id, data))
        thread.start()
        return self.response(202, task_id=task_id, message="Comprehensive analysis started")

    @expose('/get_result/<task_id>', methods=['GET'])
    def get_result(self, task_id):
        """Retrieve the result of a CrewAI task."""
        session = db.session
        task = session.query(TaskResult).filter_by(task_id=task_id).first()
        if task and task.status == 'completed':
            # Parse the JSON result
            try:
                result = json.loads(task.result)
                return self.response(200, result=result)
            except json.JSONDecodeError:
                # Fallback to returning raw result if JSON parsing fails
                return self.response(200, result=task.result)
        elif task and task.status == 'pending':
            return self.response(202, message="Task is still processing")
        elif task and task.status == 'in_progress':
            return self.response(202, message="Task is in progress")
        else:
            return self.response(404, message="Task not found or failed")
    
    @expose('/flow_visualization', methods=['GET'])
    def get_flow_visualization(self):
        """Generate and return a visualization of the comprehensive analysis flow."""
        try:
            # Import here to avoid circular dependency
            from GS.crew_ai.flows.data_analysis_flow import plot_flow
            
            # Generate a unique filename for this request
            filename = f"analysis_flow_{str(uuid4())[:8]}"
            
            # Generate the flow visualization
            visualization_path = plot_flow(output_file=filename)
            
            # If the path is returned as a URL (some environments), redirect to it
            if visualization_path.startswith('http'):
                return self.response(302, visualization_url=visualization_path)
                
            # Otherwise return the file if it exists
            if os.path.exists(visualization_path):
                return send_file(
                    visualization_path,
                    mimetype='text/html',
                    as_attachment=True,
                    download_name=f"{filename}.html"
                )
            else:
                return self.response(404, message="Visualization file not found")
        except Exception as e:
            return self.response(500, message=f"Error generating visualization: {str(e)}")