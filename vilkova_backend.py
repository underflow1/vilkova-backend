from flask import Flask, render_template, request
import sendgrid
import os
import sqlite3

DATABASE = 'database.db'
con = sqlite3.connect(DATABASE)
cursor = con.cursor()
cursor.execute('CREATE TABLE if not exists orders (id integer PRIMARY KEY, name TEXT, phone TEXT, email TEXT, quantity TEXT, amount TEXT, deliveryPrice TEXT, total TEXT)')
con.commit()
con.close()

app = Flask(__name__)

@app.route("/api/vilkova-book-order", methods=['GET'])
def hello():
    data = {}
    amount = request.args['amount']
    deliveryPrice = request.args['deliveryPrice']
    total = int(amount) + int(deliveryPrice)
    data['total'] = total
    data['amount'] = amount
    data['deliveryPrice'] = deliveryPrice
    data['name'] = request.args['name']
    data['phone'] = request.args['phone']
    data['email'] = request.args['email']
    data['quantity'] = request.args['quantity']
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute(f"INSERT INTO orders(name, phone, email, quantity, amount, deliveryPrice, total) VALUES('{data['name']}', '{data['phone']}', '{data['email']}', '{data['quantity']}', '{data['amount']}', '{data['deliveryPrice']}', '{data['total']}')")
    con.commit()
    con.close()

    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': data['email']
                    }
                ],
                'bcc': [ { 'email': os.environ.get('SHOP_EMAIL') }],
                'subject': 'VILKOVA.RU: покупка книги'
            }
        ],
        'from': {
            'email': 'no-reply@vilkova.ru'
        },
        'content': [
            {
                'type': 'text/html',
                'value': render_template('mail.html', data=data)
            }
        ]
    }
    try:
        sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

    return {"code": "OK"}

@app.route("/api/vilkova-book-info", methods=['GET'])
def info():
    con = sqlite3.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute('SELECT * FROM orders').rowcount
    rows = cursor.fetchall()
    con.commit()
    con.close()
    return {"code":"OK","ordersCount": len(rows)}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
