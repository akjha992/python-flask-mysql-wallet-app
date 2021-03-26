from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

MINIMUM_BALANCE = 150  #We can put our minimum balance requirement here


@app.route('/createNewWallet', methods=('GET', 'POST'))
def createWallet():
    if request.method == 'POST':
        req_data = request.get_json()
        phoneNumber = req_data['phoneNumber']
        initialBalance = req_data['balance']
        if not phoneNumber or not initialBalance or initialBalance < MINIMUM_BALANCE:
            return 'Invalid request!'
        else:
            cur = mysql.connection.cursor()
            try:
                resultValue = cur.execute(
                    "INSERT INTO Wallet VALUES (%s, %s)", (phoneNumber, initialBalance))
                mysql.connection.commit()
                print(resultValue)
                return 'Wallet created successfully!'
            except:
                return 'Wallet for this user already exists!', 400
            finally:
                cur.close()


@app.route('/getBalance')
def users():
    phone = request.args.get('phoneNumber')
    print(phone)
    if phone:
        cur = mysql.connection.cursor()
        query = "SELECT balance FROM Wallet WHERE phoneNumber = '{0}'".format(
            phone)
        print(query)
        resultValue = cur.execute(query)
        if resultValue > 0:
            walletDetails = cur.fetchone()[0]
            return jsonify(walletDetails)
        else:
            return 'NOT FOUND', 400
    else:
        return 'NOT FOUND', 400


@app.route('/debit', methods=('GET', 'POST'))
def debit():
    if request.method == 'POST':
        req_data = request.get_json()
        phoneNumber = req_data['phoneNumber']
        try:
            amount = float(req_data['amount'])
        except:
            amount=0
        if not phoneNumber or not amount or amount<=0:
            return 'Invalid request!'
        else:
            cur = mysql.connection.cursor()
            try:
                requiredBalance = MINIMUM_BALANCE+amount
                resultValue = cur.execute("UPDATE Wallet SET balance = balance-%s WHERE phoneNumber = %s AND balance > %s", (amount, phoneNumber, requiredBalance))
                if(resultValue == 0):
                    return 'Transaction Failed!'
                else:
                    cur.execute("INSERT INTO Transactions (PhoneNumber, Amount) values (%s, -%s)", (phoneNumber, amount))
                    mysql.connection.commit()
                    return 'Transaction Successfull!'
            except:
                return 'Transaction Failed!'
            finally:
                cur.close()


@app.route('/credit', methods=('GET', 'POST'))
def credit():
    if request.method == 'POST':
        req_data = request.get_json()
        phoneNumber = req_data['phoneNumber']
        try:
            amount = float(req_data['amount'])
        except:
            amount=0
        if not phoneNumber or not amount or amount<=0:
            return 'Invalid request!'
        else:
            cur = mysql.connection.cursor()
            try:
                resultValue = cur.execute("UPDATE Wallet SET balance = balance+%s WHERE phoneNumber = %s", (amount, phoneNumber))
                if(resultValue == 0):
                    return 'Transaction Failed!'
                else:
                    cur.execute("INSERT INTO Transactions (PhoneNumber, Amount) values (%s, %s)", (phoneNumber, amount))
                    mysql.connection.commit()
                    return 'Transaction Successfull!'
            except:
                return 'Transaction Failed!'
            finally:
                cur.close()


if __name__ == '__main__':
    app.run(debug=True)
