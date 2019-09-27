import mysql.connector
import requests
from flask import Flask,jsonify
from mysql.connector import errorcode

app = Flask(__name__)

lead = { 
	"firstName" : "Test",
	"lastName"  : "Test222",
	"email"     : "sswsrss22@gmail.com",
	"phone"     : 9899999,
	"country"   : "ITA",
	"sourceID"  : 1,
	"affID"     : 1
	}


def send_lead_rmt(lead):
        new_lead = {
                'first_name'          : lead['firstName'],
                'last_name'           : lead['lastName'],
                'email'               : lead['email'],
                'phone_number'        : lead['phone'],
                'country'             : lead['country'],
                'language'            : 'English',
                'promo_code'          : '907'
                }
        try: 
                r = requests.post('https://crm.rmt500.com/api/v2/lead', data = new_lead)
        except:
                return("no")

        r_dict = r.json()
        print(r_dict['message'])

send_lead_rmt(lead)

app.run(port=5000, debug = True)