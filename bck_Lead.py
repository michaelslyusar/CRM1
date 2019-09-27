from flask import Flask, request
from flask_restful import Resource, reqparse
import requests
import mysql.connector
import datetime
## import pdb; pdb.set_trace()


class create_lead(Resource):

    
    TABLE_NAME = 'CRM_Test5'
    
    
    def find_by_email(self, email):
        email_check = email
        connection = mysql.connector.connect(host="remotemysql.com",
                                            port=3306,
                                            user="oAJmLqZI4I",
                                            passwd="otYDdVSoi9",
                                            db="oAJmLqZI4I"
                                            )
        cursor = connection.cursor()
        query = "SELECT * FROM CRM_Test5 WHERE email = %s"
        cursor.execute(query,(email_check,))
        row = cursor.fetchone()
        

        if row:
            return {'Lead': {'Firstname': row[0], 'LastName' : row[1], 'Phone' : row[2]}}
        

    
    def post(self):
        data = request.get_json()
        email_check = data['email']
        if self.find_by_email(email_check):
            return {'message' : 'The user with the email {} is already registered'.format(data['email'])}, 404
        
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        
        lead = {
                'firstName'    : data['firstName'],
                'lastName'     : data['lastName'],
                'email'        : data['email'],
                'phone'        : data['phone'],
                'country'      : data['country'],
                'sourceID'     : data['sourceID'],
                'affID'        : data['affID'],
                'date_created' : dt_string,
                'depStatus'    : False
                }
        
        #/////Insert/////
        try:
            self.insert_db(lead)
        except:
            return {"message":"An error has occured while inserting the lead to DB{}".format(lead)}, 500
        try:
            self.send_lead_rmt(lead)
        except:
            return {"message":"An error has occured while inserting the lead to CRM{}".format(lead)}, 500
        return lead

    @classmethod
    def insert_db(cls, lead):
        connection = mysql.connector.connect(host="remotemysql.com",
                                            port=3306,
                                            user="oAJmLqZI4I",
                                            passwd="otYDdVSoi9",
                                            db="oAJmLqZI4I"
                                            )
        cursor = connection.cursor()
        
        query = "INSERT INTO {table}(firstName, lastName, email, country, phone, depStatus, sourceID, affID, date_created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table = cls.TABLE_NAME)
        cursor.execute(query, ( lead['firstName'],
                                lead['lastName'], 
                                lead['email'],
                                lead['country'],
                                lead['phone'],
                                lead['depStatus'],
                                lead['sourceID'],
                                lead['affID'],
                                lead['date_created']))

        connection.commit()
        connection. close()

    
    def send_lead_rmt(self, lead):
        
        new_lead = {
                'first_name'          : lead['firstName'],
                'last_name'           : lead['lastName'],
                'email'               : lead['email'],
                'phone_number'        : lead['phone'],
                'country'             : lead['country'],
                'language'            : 'English',
                'promo_code'          : '907'
                }
        
        r = requests.post('https://crm.rmt500.com/api/v2/lead', data = new_lead)
        r_dict = r.json()
        return {"message":"An error has occured while inserting the lead{}".format(r_dict)}

        



class get_lead_by_stat(Resource): 
    def get(self):
        connection = mysql.connector.connect(host="remotemysql.com",port=3306,user="oAJmLqZI4I",passwd="otYDdVSoi9",db="oAJmLqZI4I")
        cursor = connection.cursor()

        query = "SELECT * FROM CRM_Test5 WHERE depStatus = True"
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


    
        
        
