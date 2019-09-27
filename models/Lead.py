from flask import Flask, request
from flask_restful import Resource, reqparse
import requests
from db import db


class LeadModel(db.Model):
    __tablename__ = 'CRM_Test5'

    ID            = db.Column(db.Integer, primary_key = True)
    firstName     = db.Column(db.String(80))
    lastName      = db.Column(db.String(80))
    email         = db.Column(db.String(80))
    phone         = db.Column(db.Integer)
    country       = db.Column(db.String(80))
    sourceID      = db.Column(db.Integer)
    affID         = db.Column(db.Integer)
    date_created  = db.Column(db.Date)
    depStatus     = db.Column(db.Boolean)

    TABLE_NAME = 'CRM_Test5'

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
                'country'             : self.country,
                'language'            : 'English',
                'promo_code'          : '907'
                }
        r = requests.post('https://crm.rmt500.com/api/v2/lead', data = new_lead)
        r_dict = r.json()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()