import logging
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from flask_cors import CORS

from core.app.config import ACCEPTED_ORIGINS

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

from core.app.apis import *

from core.app.apis.example_api import ExampleApi
from core.app.models.example_model import ExampleModel

from core.app.models import *




appbuilder.add_api(ExampleApi)





db.create_all()
