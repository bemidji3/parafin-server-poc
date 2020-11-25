#!/usr/bin/env python3
from flask import Flask, request, send_file
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open('.secret', 'r') as f:
    secrets = json.loads(f.read())
    api_key = secrets["api_key"]
    vendor_stats = secrets["user"]


@app.route('/new-loan', methods=['POST'])
def loan_create():
    my_request = request.get_json()

    print(my_request)

    db_entry = build_db_entry(my_request)
    res = write_to_file(db_entry)

    if res:
        return json.loads('{ "status": 200 }')
    else:
        return json.loads('{ "status" : 400, "error" : "api_key" }')


@app.route('/get-vendor-information', methods=['GET'])
def get_vendor_info():
    return vendor_stats


@app.route('/get-loan-stats', methods=['GET'])
def get_loan_stats():
    return send_file('db/db.txt', attachment_filename='database.txt')


def write_to_file(my_request):
    print('writing to file')
    with open("db/db.txt", "a") as my_file:
        my_file.write(str(my_request) + ",\n")
    return True


def build_db_entry(my_request):
    db_entry = {
        'business_name': my_request['business_name'],
        'business_description': my_request['business_description'],
        'loan_amount': my_request['loan_amount']
    }

    return str(db_entry)


if __name__ == '__main__':
    app.run()