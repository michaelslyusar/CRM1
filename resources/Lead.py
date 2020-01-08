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
        
        lead = LeadModel(data['firstName'],data['lastName'],data['email'],data['phone'],data['country'],data['ip'],data['prefix'],data['sourceID'],data['affID'],dt_string,False)
        
        #Inserting to DB
        try:
            lead.save_to_db()
            if(data['affID'] == "12"):
                r = LeadModel.send_lead_branding(lead)
                message = r['status']
                if(message == 1 or message == 'true'):
                    return {'message' : 'Lead created successfully'}, 201
                else:
                    return {'message' : 'Something went wrong:{}'.format(r['data'])}, 500
            return {'message' : 'Lead created successfully'}, 201
        except Exception as e:
            LeadModel.logger("message : Something went wrong when inserting to DB {}".format(e))
            return {"message":"An error has occured while inserting the lead to DB{}".format(e)}, 500


        
        #if(data['affID'] == 12):   #######Branding
        #Inserting to Branding
            #r = LeadModel.send_lead_branding(lead)
            #message = r['message']
            #try:
            #    if(message == 'OK'):
            #        return {'message' : 'Lead created successfully'}, 201
            #    else:
            #        return {'message' : 'Something went wrong:{}'.format(r)}, 500
            #except Exception as e:
            #    LeadModel.logger("message : Something went wrong when inserting into CRM{}".format(e))


        #Inserting to CRM
        #r = LeadModel.send_lead_rmt(lead)
        #message = r['message']
        #try:
        #    if(message == 'OK'):
        #        return {'message' : 'Lead created successfully'}, 201
        #    else:
        #        return {'message' : 'Something went wrong:{}'.format(r)}, 500
        #except Exception as e:
        #    LeadModel.logger("message : Something went wrong when inserting into CRM{}".format(e))


