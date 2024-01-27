from flask import Flask, request, jsonify, Response, render_template, url_for, flash, redirect, session, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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
import logging
import subprocess
import ast
from dml_sql import add_order, add_customer, add_user, edit_customer, add_company
from db_sql import get_db_customers, get_order_list, get_customer_list, get_order_detail, get_customer_detail, \
    get_order_list_by_customer, get_user, get_report_data, get_db_companies, get_db_companies_detail, get_company_list,get_company_detail


log_filename = '/var/log/cashchecking.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename=log_filename,
                    filemode='w',
                    force=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = '5UUh-uNiJMZ<{qWx00z:f!/to|aT0('
# app.config['SERVER_NAME'] = '47.188.174.139:80'

#17644 Is where the load stops, anything from Conoco will be marked with 'C' after. So if conoco id was 100 it will be 100C

########################################AUTH#################################################################

class User():
    def __init__(self, is_active, id, username):
        self.is_active = is_active
        self.id = id
        self.username = username

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True


def get_sqlite_connection():
    conn = sqlite3.connect('cashchecking.db')
    cur = conn.cursor()
    return conn, cur


def is_admin():
    try:
        conn, cursor = get_sqlite_connection()
        id = current_user.id
        cursor.execute(f''' select permission from employees where employee_id = {id}''')
        permission = cursor.fetchone()[0]
    except Exception as e:
        return False
    finally:
        conn.commit()
        conn.close()
    if permission.lower() == 'admin':
        return True
    else:
        return False



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'cashchecking_icon.png')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     user = User(username=username, password=password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Registration successful. Please log in.')
    #     return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            conn, cursor = get_sqlite_connection()
            username = request.form['username']
            password = request.form['password']
            user_result = get_user(cursor, password, username)
            id = user_result[0]
            username = username
            user = User(True, id, username)
            if user:
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Login failed. Please check your credentials.')
        return render_template('login.html')
    except Exception as e:
        return render_template('login.html')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    conn, cursor = get_sqlite_connection()
    cursor.execute(f'''select username from employees where employee_id = {user_id}''')
    username = cursor.fetchone()[0]
    return User(True, user_id, username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))


#########################################################################################################
def save_image(request, url):
    try:
        image_data_url = request.form['imageDataUrl']
        uuid = request.form['uuid']

        with open(f'./static/images/{url}/{uuid}.png', 'wb') as file:
            file.write(base64.b64decode(image_data_url.split(',')[1]))

            return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, error=str(e))


@app.route('/webhooks', methods=['GET','POST'])
def webhooks():
    logging.info(f"I am here")
    try:
        cmd1 = "touch /home/ubuntu/touch.txt"

        os.system(cmd1)
        logging.info(f"{cmd1} done")
        cmd = "bash /home/ubuntu/flask_app/cashchecking/cici.sh"
        os.system(cmd1)
        logging.info(f"{cmd} done")
    except Exception as e:
        logging.info(f"{e}")

    return 'hello'

@app.route('/upload_image', methods=['POST'])
def upload_image():
    return save_image(request, 'customer_photo')


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
    try:
        admin = is_admin()
    except Exception as e:
        admin = False
    return render_template('home.html', admin=admin)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    store = request.args.get('store', None, type=str)
    if store == 'None':
        store = None
    date_to = request.args.get('date_to', '', type=str)
    date_from = request.args.get('date_from', '', type=str)
    text = request.args.get('search_text', '', type=str)
    page = request.args.get('page', 1, type=int)
    conn, cursor = get_sqlite_connection()
    results = get_order_list(cursor, date_from, date_to, text, store)
    paginated_customers = results[(page - 1) * 100:page * 100]
    has_next = len(results[(page) * 100:(page + 1) * 100])
    has_prev = len(results[(page - 2) * 100:(page - 1) * 100])
    conn.close()
    all_orders = []
    print("Date from:", date_from)
    print("Date to:", date_to)

    for result in paginated_customers:
        order_detail = {}
        order_detail['order_number'] = result[0]
        order_detail['customer_id'] = result[1]
        order_detail['order_create_date'] = result[2]
        order_detail['date_check_issued'] = result[3]
        order_detail['check_number'] = result[4]
        order_detail['amount'] = result[5]
        order_detail['amount_issued'] = result[6]
        order_detail['store'] = result[7]
        all_orders.append(order_detail)

    return render_template('orders.html', orders_list=all_orders, has_next=has_next, current_page=page,
                           has_prev=has_prev, store=store, search_text=text, date_from= date_from, date_to=date_to)

@app.route('/companies', methods=['GET', 'POST'])
@login_required
def companies():
    date_to = request.args.get('date_to', '', type=str)
    date_from = request.args.get('date_from', '', type=str)
    text = request.args.get('search_text', '', type=str)
    page = request.args.get('page', 1, type=int)
    conn, cursor = get_sqlite_connection()
    results = get_company_list(cursor, date_from, date_to, text)
    paginated_customers = results[(page - 1) * 100:page * 100]
    has_next = len(results[(page) * 100:(page + 1) * 100])
    has_prev = len(results[(page - 2) * 100:(page - 1) * 100])
    conn.close()
    all_orders = []

    for result in paginated_customers:
        company = {}
        company['company_id'] = result[0]
        company['name'] = result[1]
        company['address'] = result[2]
        company['phone_number'] = result[3]
        company['creation_date'] = result[4]
        all_orders.append(company)
    return render_template('companies.html', orders_list=all_orders, has_next=has_next, current_page=page,
                           has_prev=has_prev, search_text=text, date_from=date_from, date_to=date_to)




@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    store = request.args.get('store', None, type=str)
    if store == 'None':
        store = None
    date_to = request.args.get('date_to', '', type=str)
    date_from = request.args.get('date_from', '', type=str)
    text = request.args.get('search_text', '', type=str)
    page = request.args.get('page', 1, type=int)
    conn, cursor = get_sqlite_connection()
    results = get_customer_list(cursor, date_to, date_from, text, store)
    paginated_customers = results[(page - 1) * 100:page * 100]
    has_next = len(results[(page) * 100:(page + 1) * 100])
    has_prev = len(results[(page - 2) * 100:(page - 1) * 100])
    conn.close()

    print(text)
    all_customers = []
    for result in paginated_customers:
        order_detail = {}
        order_detail['customer_id'] = result[0]
        order_detail['first_name'] = result[1]
        order_detail['last_name'] = result[2]
        order_detail['phone_number'] = result[3]
        order_detail['address'] = result[4]
        order_detail['license_number'] = result[5]
        order_detail['account_creation'] = result[6]
        order_detail['last_checked'] = result[7]
        order_detail['store'] = result[8]
        all_customers.append(order_detail)
    return render_template('customers.html', orders_list=all_customers, has_next=has_next, current_page=page,
                           has_prev=has_prev, search_text=text, store=store, date_from= date_from, date_to=date_to)



@app.route('/company/<company_id>')
@login_required
def company_detail(company_id):
    conn, cursor = get_sqlite_connection()
    comp, order, customer = get_company_detail(cursor, company_id)
    conn.close()
    comp = {
        'company_id': comp[0],
        'name': comp[1],
        'address': comp[2],
        'phone_number': comp[3],
        'creation_date': comp[4],
    }

    return render_template('company_detail.html', order=order, company=comp, customer=customer)

@app.route('/customer/<customer_id>', methods=['GET', 'POST'])
@login_required
def customer_detail(customer_id):
    if request.method == 'POST':
        headers = request.headers
        conn, cursor = get_sqlite_connection()
        result = get_customer_detail(cursor, customer_id)
        orders_list = get_order_list_by_customer(cursor, customer_id)
        result = result[0]
        conn.close()
        customer = {
            'id': customer_id,
            'first_name': result[1],
            'last_name': result[2],
            'phone_number': result[3],
            'address': result[4],
            'license_number': result[5],
            'account_creation': result[6],
            'last_checked': result[7],
            'uuid': result[8],
            'is_flagged': result[9],
            'store': result[11],
            'notes': result[10],
            'old_id': result[12]
        }
        customer_orders = []
        for order in orders_list:
            new_dict = {'order_number': order[0], 'order_create_date': order[2], 'date_check_issued': order[3],
                        'check_number': order[4], 'amount': order[5], 'amount_issued': order[7]}
            customer_orders.append(new_dict)

        if headers['request'] == 'customer':
            return customer
        elif headers['request'] == 'order_list':
            return customer_orders

    conn, cursor = get_sqlite_connection()
    result = get_customer_detail(cursor, customer_id)
    orders_list = get_order_list_by_customer(cursor, customer_id)
    result = result[0]
    conn.close()
    customer = {
        'id': customer_id,
        'first_name': result[1],
        'last_name': result[2],
        'phone_number': result[3],
        'address': result[4],
        'license_number': result[5],
        'account_creation': result[6],
        'last_checked': result[7],
        'uuid': result[8],
        'is_flagged': result[9],
        'store': result[11],
        'notes': result[10],
        'old_id': result[12]
    }
    customer_orders = []
    for order in orders_list:
        new_dict = {'order_number': order[0], 'order_create_date': order[2], 'date_check_issued': order[3],
                    'check_number': order[4], 'amount': order[5], 'amount_issued': order[7]}
        customer_orders.append(new_dict)
    return render_template('customer_detail.html', customer=customer, customer_orders=customer_orders)


@app.route('/order/<order_id>')
@login_required
def order_detail(order_id):
    conn, cursor = get_sqlite_connection()
    result = get_order_detail(cursor, order_id)
    result = result[0]
    conn.close()
    order = {
        'order_number': order_id,
        'customer_id': result[1],
        'order_create_date': result[2],
        'date_check_issued': result[3],
        'check_number': result[4],
        'amount': result[5],
        'uuid': result[6],
        'amount_issued': result[7]
    }

    return render_template('order_detail.html', order=order)


@app.route('/reports', methods=['GET'])
@login_required
def reports():
    return render_template('reports.html')


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    admin = is_admin()
    return render_template('admin.html', admin=admin)


@app.route('/new_order', methods=['GET', 'POST'])
@login_required
def new_order():
    uuid = uuid4().hex
    return render_template('new_order.html', uuid=uuid)


@app.route('/new_customer', methods=['GET', 'POST'])
@login_required
def new_customer():
    uuid = uuid4().hex
    return render_template('new_customer.html', uuid=uuid)


@app.route('/order_list')
def orders_list():
    pass


@app.route('/get_customers', methods=['GET','POST'])
def get_customers():
    conn, cursor = get_sqlite_connection()
    results = get_db_customers(cursor)
    # print(results)
    conn.close()
    customer_list = []
    for customer in results:
        old_id = '-' + str(customer[5]) + "C" if customer[5] else ""
        customer_string = f'{customer[0]}{f"-{customer[1].upper()}" if customer[1] else ""}{f"-{customer[2].upper()}" if customer[2] else ""}{"-FLAGGED" if customer[4] == 1 else ""}{old_id}'
        customer_list.append(customer_string)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    query = request.args.get('query', '', type=str)
    filtered_customers = [c for c in customer_list if
                          query.lower() in c.lower() or query.lower() in c.lower().replace('-', ' ')]
    paginated_customers = filtered_customers[(page - 1) * limit:page * limit]

    return jsonify(paginated_customers)


@app.route('/get_companies', methods=['POST'])
def get_companies():
    filter = request.get_json()
    filter= filter['filter']
    conn, cursor = get_sqlite_connection()
    results = get_db_companies(cursor, filter)
    conn.close()
    new_dict = [{'name': item[0]} for item in results]
    return new_dict

@app.route('/get_company_details', methods=['POST'])
def get_company_details():
    filter = request.get_json()
    filter= filter['companyName']
    conn, cursor = get_sqlite_connection()
    results = get_db_companies_detail(cursor, filter)
    conn.close()
    details = {'address':results[0], 'phone': results[1]}
    return details

@app.route('/save_notes', methods=['POST'])
def save_notes():
    data = request.data.decode("utf-8")
    data = ast.literal_eval(data)
    notes = data['notes']
    customer_id = data['customerId'].split(':')[-1].replace('}', '').replace('"', '').replace(' ', '')
    conn, cursor = get_sqlite_connection()
    sql = f''' update customers set notes = '{notes}' where customer_id = {customer_id}'''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify(success=True)


@app.route('/flag_account', methods=['POST'])
def flag_account():
    data = request.data.decode("utf-8")
    id = data.split(':')[-1].replace('}', '').replace('"', '').replace(' ', '')
    conn, cursor = get_sqlite_connection()
    sql = f''' update customers set is_flagged = 1 where customer_id = {id}'''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify(success=True)


@app.route('/unflag_account', methods=['POST'])
def unflag_account():
    data = request.data.decode("utf-8")
    id = data.split(':')[-1].replace('}', '').replace('"', '').replace(' ', '')
    conn, cursor = get_sqlite_connection()
    sql = f''' update customers set is_flagged = 0 where customer_id = {id}'''
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify(success=True)


############# FORMS ############################################################
@app.route('/order_submit', methods=['POST'])
def order_submit():
    conn, cursor = get_sqlite_connection()
    data = request.form
    employee_id = current_user.id
    time_now = datetime.datetime.now().isoformat()
    company_id = add_company(cursor, data, employee_id, time_now)
    add_order(cursor, data, employee_id, time_now, company_id)
    edit_customer(cursor, data, time_now)
    conn.commit()
    conn.close()
    return render_template('home.html', submit_order=True)


@app.route('/customer_submit', methods=['POST'])
def customer_submit():
    conn, cursor = get_sqlite_connection()
    data = request.form
    employee_id = current_user.id
    time_now = datetime.datetime.now().isoformat()
    add_customer(cursor, data, employee_id, time_now)
    conn.commit()
    conn.close()
    return render_template('home.html', submit_customer=True)


@app.route('/add_user', methods=['POST'])
def add_new_user():
    conn, cursor = get_sqlite_connection()
    data = request.form
    print(data)
    add_user(cursor, data)
    conn.commit()
    conn.close()
    admin = is_admin()
    return render_template('admin.html', admin=admin)


@app.route('/report_data', methods=['POST'])
def report_data():
    headers = request.headers
    date_to = headers['DateTo']
    date_from = headers['DateFrom']
    conn, cursor = get_sqlite_connection()
    results = get_report_data(cursor, date_to, date_from)
    conn.commit()
    conn.close()
    all_orders = []

    for row in results:
        json_temp = {
            'order_id': row[0],
            'customer_id': row[1],
            'order_create_date': row[2],
            'amount': row[3],
            'employee_id': row[4],
            'amount_issued': row[5],
            'store': row[6]
        }
        all_orders.append(json_temp)
    admin = is_admin()
    return_results = {'all_results': all_orders}
    return jsonify(return_results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
