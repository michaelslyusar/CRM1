import os
from flask import Flask, request
from flask_restful import Api
from resources.Lead import get_lead_by_stat, create_lead
import sys
import logging

app = Flask(__name__)

app.config['DEBUG'] = True

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Aa123456@database-4.crywuregr34q.eu-central-1.rds.amazonaws.com:3306/crm159'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


api.add_resource(create_lead, '/create_lead')
api.add_resource(get_lead_by_stat, '/LeadList_dep')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
