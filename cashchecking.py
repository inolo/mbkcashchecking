from flask import Flask, request, jsonify, Response, render_template
import base64
import json
import hmac
import hashlib
import datetime
import base64
from uuid import uuid4
import os
import sqlite3
import time
import os
import secrets
import sys
import requests
import numpy as np
from threading import Thread


app = Flask(__name__)


def save_image(request,url):
    try:
        # customerNumber = request.form['customerNumber']
        image_data_url = request.form['imageDataUrl']
        # checkNumber = request.form['checkNumber']
        uuid = request.form['uuid']

        with open(f'./static/images/{url}/{uuid}.png', 'wb') as file:
            file.write(base64.b64decode(image_data_url.split(',')[1]))

            return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, error=str(e))


@app.route('/upload_image', methods=['POST'])
def upload_image():
    return save_image(request,'customer_photo')

@app.route('/upload_license_image', methods=['POST'])
def upload_license_image():
    return save_image(request, 'license_copy')

@app.route('/upload_check_copy', methods=['POST'])
def upload_check_copy():
    return save_image(request, 'check_images')


@app.route('/webcam')
def webcam():
    return render_template('webcam.html')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/orders', methods=['GET'])
def orders():
    return 'This is the order page'

@app.route('/customers', methods=['GET'])
def customers():
    return 'This is the customer page'

@app.route('/reports', methods=['GET'])
def reports():
    return 'This is the reports page'


@app.route('/new_order', methods=['GET'])
def new_order():
    uuid = uuid4().hex
    return render_template('new_order.html',uuid=uuid)

@app.route('/new_customer', methods=['GET'])
def new_customer():
    uuid = uuid4().hex
    return render_template('new_customer.html',uuid=uuid)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)