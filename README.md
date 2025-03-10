SET FLASK_APP=core/app/__init__.py

flask fab create-admin


SET FLASK_APP=app/__init__.py

flask db init

flask db migrate

flask db upgrade
