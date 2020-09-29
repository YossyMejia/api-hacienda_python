from flask import Flask, jsonify
from extensions import mysql
from configuration import globalsettings
import connexion
from helpers import debugging
from helpers.errors import handlers as errorhandlers

app = Flask(__name__)
cfg = globalsettings.cfg

app.config['MYSQL_DATABASE_USER'] = cfg['mysql']['user']
app.config['MYSQL_DATABASE_PASSWORD'] = cfg['mysql']['passwd']
app.config['MYSQL_DATABASE_DB'] = cfg['mysql']['db']
app.config['MYSQL_DATABASE_HOST'] = cfg['mysql']['host']
mysql.init_app(app)
options = {'swagger_path': '/api/swagger_ui/'}
spec_args = {'debug_switch' : debugging.DEBUG_SWITCH_NAME}
app = connexion.App(__name__, specification_dir='./', options=options)
app.add_api('api-hacienda.yaml',arguments=spec_args)

# Sets custom error handlers for application error responses.
errorhandlers.register_flask_app_handlers(app)

app.run(host='localhost', port=3005)

