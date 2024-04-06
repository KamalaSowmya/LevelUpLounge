from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'leveluploungedb'
 
mysql = MySQL(app)

# search content from posts 
@app.route('/')
@app.route('/search', methods =['GET']) 
def search():
    query = request.args.get('query')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sqlquery = "SELECT * FROM publications WHERE content LIKE "+ "'%" + query + "%'"
    print(sqlquery)
    cursor.execute(sqlquery)
    details = cursor.fetchall()
    print(details)
    if details:            
        msg = 'Found posts with this keyword !'
        response = {
            "message"  : msg, 
        }
        return jsonify(details)
    else:
        msg = 'No posts found on this!'
    details  = {
        "message" : msg 
    }
    return jsonify(details)

#serach for users
@app.route('/')
@app.route('/searchUser', methods =['GET']) 
def searchUser():
    user = request.args.get('user')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sqlquery = "SELECT username FROM userdetails WHERE username LIKE "+ "'%" + user + "%'"
    print(sqlquery)
    cursor.execute(sqlquery)
    details = cursor.fetchall()
    print(details)
    if details:            
        msg = 'Found posts with this keyword !'
        response = {
            "message"  : msg, 
        }
        return jsonify(details)
    else:
        msg = 'No posts found on this!'
    details  = {
        "message" : msg 
    }
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

print("Done!")