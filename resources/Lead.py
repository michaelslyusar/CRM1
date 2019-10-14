from flask import Flask, request
from flask_restful import Resource, reqparse
import requests
import datetime
from models.Lead import LeadModel

class create_lead(Resource):

    def post(self):
        data = request.get_json()
        email_check = data['email']
        if LeadModel.find_by_email(email_check):
            return {'message' : 'The user with the email {} is already registered'.format(data['email'])}, 404
        
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        
        lead = LeadModel(data['firstName'],data['lastName'],data['email'],data['phone'],data['country'],data['sourceID'],data['affID'],dt_string,False)
        
        #Inserting to DB
        try:
            lead.save_to_db()
        except Exception as e:
            LeadModel.logger("message : Something went wrong when inserting to DB {}".format(e))
            return {"message":"An error has occured while inserting the lead to DB{}".format(e)}, 500

            
        #Inserting to CRM
        r = LeadModel.send_lead_rmt(lead)
        message = r['message']
        try:
            if(message == 'OK'):
                return {'message' : 'Lead created successfully'}, 201
            else:
                return {'message' : 'Something went wrong:{}'.format(r)}, 500
        except Exception as e:
            LeadModel.logger("message : Something went wrong when inserting into CRM{}".format(e))



class get_lead_by_stat(Resource): 
    def get(self):
        connection = mysql.connector.connect(host="remotemysql.com",port=3306,user="oAJmLqZI4I",passwd="otYDdVSoi9",db="oAJmLqZI4I")
        cursor = connection.cursor()

        query = "SELECT * FROM CRM_Production WHERE depStatus = True"
        cursor.execute(query)
        Leads = cursor.fetchall()
        
        connection.close()
        results = []
        a = 1
        for Lead in Leads:
            temp  = {'ID' : a, 'email' : Lead[3], 'depStatus' : Lead[6]}
            results.append(temp)
            a = a+1

        if not results:
            return {'message' : 'no leads'}
        else:
            return results
