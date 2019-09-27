from flask import Flask, request
from flask_restful import Api
from Lead import get_lead_by_stat, create_lead


app = Flask(__name__)
api = Api(app)


api.add_resource(create_lead, '/create_lead')
api.add_resource(get_lead_by_stat, '/LeadList_dep')


if __name__ == '__main__':
    app.run(port=5000, debug = True)