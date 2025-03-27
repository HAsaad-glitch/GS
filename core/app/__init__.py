import logging
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from flask_cors import CORS

from GS.core.app.config import ACCEPTED_ORIGINS
from GS.core.app.models.task_result import TaskResult

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
cors = CORS(app, origins=ACCEPTED_ORIGINS)
app.config.from_pyfile("config.py")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

migrate = Migrate(app, db)

# Import APIs after db is initialized
from GS.core.app.apis.crewai_api import CrewAIApi
appbuilder.add_api(CrewAIApi)

db.create_all()
