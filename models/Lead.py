from flask import Flask, request
from flask_restful import Resource, reqparse
import requests
from db import db
import logging

class LeadModel(db.Model):
    __tablename__ = 'CRM_K'

    ID            = db.Column(db.Integer, primary_key = True)
    firstName     = db.Column(db.String(30))
    lastName      = db.Column(db.String(30))
    email         = db.Column(db.String(30))
    phone         = db.Column(db.String(30))
    country       = db.Column(db.String(30))
    sourceID      = db.Column(db.String(80))
    affID         = db.Column(db.Integer)
    date_created  = db.Column(db.Date)
    depStatus     = db.Column(db.Boolean)

    TABLE_NAME = 'CRM_K'

    def __init__(self, firstName, lastName, email, phone, country, sourceID, affID, date_created, depStatus):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone  
        self.country = country   
        self.sourceID = sourceID 
        self.affID = affID     
        self.date_created = date_created
        self.depStatus = depStatus
        
    
    def json(self):
        return{'firsName' : self.firstName,
                'lastName' :self.lastName,
                'email' :self.email,
                'phone' :self.phone, 
                'country' :self.country,   
                'sourceID' :self.sourceID, 
                'affID' :self.affID,     
                'date_created' :self.date_created,
                'depStatus' :self.depStatus}

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def send_lead_rmt(self):
        new_lead = {
                'first_name'          : self.firstName,
                'last_name'           : self.lastName,
                'email'               : self.email,
                'phone_number'        : self.phone,
                'country'             : self.country,  #ISO 3166-1 alpha-2; ISO 3166-1 alpha-3
                'language'            : 'Italian',
                'promo_code'          : '128'
                }
        try:
            r = requests.post('https://crm.rmt500.com/api/v2/lead', data = new_lead)
        except Exception as e:
            return e
        r_dict = r.json()
        return(r_dict)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    

    def logger(string):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('sample.log')
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        logger.error(string)
