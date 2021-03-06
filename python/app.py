import os
import requests
import sqlite3
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, jsonify, request

pwd = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

SCOPES=['openid','https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

@app.route("/start", methods=["GET"])
def start():
    flow = Flow.from_client_secrets_file(
        os.path.join(pwd,'credentials.json'),
        scopes=SCOPES,
        redirect_uri='http://localhost:5000/callback')

    auth_uri = flow.authorization_url()

    return jsonify(auth_uri[0]), 200

@app.route("/callback", methods=["GET"])
def callback():
    try:
        flow = Flow.from_client_secrets_file(
            os.path.join(pwd,'credentials.json'),
            scopes=SCOPES,
            redirect_uri='http://localhost:5000/callback')

        code = request.args.get("code", default="", type=str)
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # store in db
        conn = sqlite3.connect('test.db')

        print ("Opened database successfully")

        conn.execute("CREATE TABLE GRANTS (ID INT PRIMARY KEY NOT NULL, TOKEN TEXT NOT NULL);")
        print ("Table created successfully")
        
        conn.execute("INSERT INTO GRANTS (ID, TOKEN) \
        VALUES (1, ?)", [credentials.to_json()]);
        conn.commit()
        print ("Tokens created successfully");
        conn.close()
        # # Save the credentials for the next run
        # with open('token.json', 'w') as token:
        #     token.write(credentials.to_json())

        return "http://localhost:5000/email", 200
    except HttpError as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500
    except Exception as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500

@app.route("/email", methods=["GET"])
def email():
    try:
        conn = sqlite3.connect('test.db')

        print ("Opened database successfully")
        cursor = conn.execute("SELECT * FROM GRANTS")
        for row in cursor:
            creds = json.loads(row[1])

        conn.close()

        creds = Credentials.from_authorized_user_info(creds, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
        # Optionally, view the email address of the authenticated user.
        user_info_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_info_service.userinfo().get().execute()

        return jsonify(user_info['email']), 200
    except HttpError as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500
    except Exception as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500

@app.route("/revoke", methods=["GET"])
def revoke():
    try:
        conn = sqlite3.connect('test.db')

        print ("Opened database successfully")
        cursor = conn.execute("SELECT * FROM GRANTS")
        for row in cursor:
            creds = json.loads(row[1])

        conn.close()
        
        creds = Credentials.from_authorized_user_info(creds, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
        revoke = requests.post('https://oauth2.googleapis.com/revoke', params={'token': creds.token}, headers = {'content-type': 'application/x-www-form-urlencoded'})

        status_code = getattr(revoke, 'status_code')
        if status_code == 200:
            return jsonify("Credentials successfully revoked."), 200
        else:
            raise Exception(getattr(revoke, 'reason'))

    except HttpError as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500
    except Exception as error:
        print(f'An error occurred: {error}')
        return "internal server error", 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)