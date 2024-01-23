from flask import Flask, request, jsonify, Response, render_template, url_for, flash, redirect
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
from dml_sql import add_order, add_customer
from db_sql import get_db_customers, get_order_list, get_customer_list, get_order_detail, get_customer_detail, get_order_list_by_customer


app = Flask(__name__)
app.config['SECRET_KEY'] = '5UUh-uNiJMZ<{qWx00z:f!/to|aT0('


def get_sqlite_connection():
    conn = sqlite3.connect('cashchecking.db')
    cur = conn.cursor()
    return conn, cur

def save_image(request, url):
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

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    date_to = request.args.get('date_to', '', type=str)
    date_from = request.args.get('date_from', '', type=str)
    text = request.args.get('search_text', '', type=str)
    page = request.args.get('page', 1, type=int)
    conn, cursor = get_sqlite_connection()
    results = get_order_list(cursor, date_to, date_from, text)
    paginated_customers = results[(page - 1) * 100:page * 100]
    has_next = len(results[(page) * 100:(page+1) * 100])
    has_prev = len(results[(page-2) * 100:(page-1) * 100])
    conn.close()
    all_orders = []

    for result in paginated_customers:
        order_detail = {}
        order_detail['order_number'] = result[0]
        order_detail['customer_id'] = result[1]
        order_detail['order_create_date'] = result[2]
        order_detail['date_check_issued'] = result[3]
        order_detail['check_number'] = result[4]
        order_detail['amount'] = result[5]
        all_orders.append(order_detail)

    return render_template('orders.html', orders_list=all_orders, has_next=has_next, current_page=page, has_prev=has_prev)



@app.route('/customers', methods=['GET', 'POST'])
def customers():
    date_to = request.args.get('date_to', '', type=str)
    date_from = request.args.get('date_from', '', type=str)
    text = request.args.get('search_text', '', type=str)
    page = request.args.get('page', 1, type=int)
    conn, cursor = get_sqlite_connection()
    results = get_customer_list(cursor, date_to, date_from, text)
    paginated_customers = results[(page - 1) * 100:page * 100]
    has_next = len(results[(page) * 100:(page+1) * 100])
    has_prev = len(results[(page-2) * 100:(page-1) * 100])
    conn.close()
    all_customers = []

    for result in paginated_customers:
        print(result)
        order_detail = {}
        order_detail['customer_id'] = result[0]
        order_detail['first_name'] = result[1]
        order_detail['last_name'] = result[2]
        order_detail['phone_number'] = result[3]
        order_detail['address'] = result[4]
        order_detail['license_number'] = result[5]
        order_detail['account_creation'] = result[6]
        order_detail['last_checked'] = result[7]
        all_customers.append(order_detail)
    return render_template('customers.html', orders_list=all_customers, has_next=has_next, current_page=page, has_prev=has_prev)


@app.route('/customer/<customer_id>')
def customer_detail(customer_id):
    conn, cursor = get_sqlite_connection()
    result = get_customer_detail(cursor, customer_id)
    orders_list = get_order_list_by_customer(cursor, customer_id)
    result = result[0]
    conn.close()
    # Dummy data for illustration
    customer = {
        'id': customer_id,
        'first_name': result[1],
        'last_name': result[2],
        'phone_number': result[3],
        'address': result[4],
        'license_number': result[5],
        'account_creation': result[6],
        'last_checked': result[7],
        'uuid': result[8]
    }
    customer_orders = []
    for order in orders_list:
        new_dict =  {'order_number': order[0], 'order_create_date': order[2], 'date_check_issued': order[3], 'check_number': order[4], 'amount': order[5]}
        customer_orders.append(new_dict)
    return render_template('customer_detail.html', customer=customer, customer_orders=customer_orders)

@app.route('/order/<order_id>')
def order_detail(order_id):
    conn, cursor = get_sqlite_connection()
    # Fetch order details based on order_id
    # For example: order = Order.query.get(order_id)
    result = get_order_detail(cursor, order_id)
    result = result[0]
    conn.close()
    # Dummy data for illustration
    order = {
        'order_number': order_id,
        'customer_id': result[1],
        'order_create_date': result[2],
        'date_check_issued': result[3],
        'check_number': result[4],
        'amount': result[5],
        'uuid': result[6]
    }

    return render_template('order_detail.html', order=order)


@app.route('/reports', methods=['GET'])
def reports():
    return 'This is the reports page'

@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    uuid = uuid4().hex
    return render_template('new_order.html',uuid=uuid)

@app.route('/new_customer', methods=['GET','POST'])
def new_customer():
    uuid = uuid4().hex
    return render_template('new_customer.html',uuid=uuid)

@app.route('/order_list')
def orders_list():
    pass

@app.route('/get_customers')
def get_customers():
    conn, cursor = get_sqlite_connection()
    results = get_db_customers(cursor)
    conn.close()
    customer_list = []
    for customer in results:
        customer_string = f'{customer[0]}-{customer[1]}-{customer[2]}-{customer[3]}'
        customer_list.append(customer_string)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    query = request.args.get('query', '', type=str)
    # Implement search and pagination logic
    # For simplicity, this example just slices the customer list
    filtered_customers = [c for c in customer_list if query.lower() in c.lower() or query.lower() in c.lower().replace('-', ' ')]
    paginated_customers = filtered_customers[(page-1)*limit:page*limit]

    return jsonify(paginated_customers)

############# FORMS ############################################################
@app.route('/order_submit', methods=['POST'])
def order_submit():
    conn, cursor = get_sqlite_connection()
    data = request.form
    employee_id = 1
    # data['customer_uuid'] = 11
    add_order(cursor, data, employee_id)
    conn.commit()
    conn.close()
    return render_template('home.html', submit_order=True)


@app.route('/customer_submit', methods=['POST'])
def customer_submit():
    conn, cursor = get_sqlite_connection()
    data = request.form
    add_customer(cursor, data)
    conn.commit()
    conn.close()
    return render_template('home.html', submit_customer=True)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)