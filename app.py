from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_mail import Mail
import MySQLdb.cursors
import re

app = Flask(__name__)
#app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'leveluploungedb'
 
mysql = MySQL(app)

# Login 
@app.route('/')
@app.route('/login', methods =['POST']) #or just POST would do
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userdetails WHERE email = %s AND password = %s', (email, password, ))
        details = cursor.fetchone()
        if details:            
            msg = 'Logged in successfully !'
            response = {
                "message" : msg 
            }
            return jsonify(response)
        else:
            msg = 'Incorrect email / password !'
    response = {
        "message" : msg 
    }
    return jsonify(response)

#Registration
@app.route('/register', methods =['POST'])
def register():
    msg = ''
    success = False
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(username, password, email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userdetails WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account with specified details exists already!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must be alphanumeric only!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email id!'

        elif not username or not password or not email:
            msg = 'Please fill all the details in form'

        else:
            cursor.execute('INSERT INTO userdetails VALUES ( %s, %s, %s)', (username, email, password ))
            mysql.connection.commit()
            success = True

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        
    response = {
        "Error" : msg,
        "success" : success  
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
print("End!")