import os
import sqlite3
from flask import Flask, render_template, jsonify, url_for, redirect
app = Flask(__name__)

DATABASE_LOCATION = '/Users/bermudez/Documents/personal/gitprojects/ise/database'
DATABASE_NAME = 'sse.db'
ABS_PATH = os.path.join(DATABASE_LOCATION, DATABASE_NAME)

# One master connection?
#connection = sqlite3.connect(ABS_PATH)
#cursor = connection.cursor()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/api/tables')
def list_tables():
    tables = []
    with sqlite3.connect(ABS_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        response = cursor.fetchall()
        for table in response:
            tables.append(table[0])
        return str(tables)


@app.route('/api/tables/<tablename>')
def query_table(tablename):
    response = ''
    with sqlite3.connect(ABS_PATH) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(tablename))
            all_rows = cursor.fetchall()
            for row in all_rows:
                response += '{0} | {1} | {2}<br/>'.format(row[0], row[1], row[2])
            return str(response)
        except Exception as e:
            return str(e)


@app.route('/api/tables/last/<tablename>')
def query_table_last_entry(tablename):
    with sqlite3.connect(ABS_PATH) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(tablename))
            all_rows = cursor.fetchall()
            last_entry = '{0} | {1} | {2}'.format(all_rows[-1][0], all_rows[-1][1], all_rows[-1][2])
            return str(last_entry)
        except Exception as e:
            return str(e)


@app.route('/api/services/status')
def score_board():
    services_last_status = {}
    with sqlite3.connect(ABS_PATH) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_name_response = cursor.fetchall()
            for table in table_name_response:
                table_name = table[0]
                cursor.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table_name))
                last_entry_response = cursor.fetchone()
                last_entry_status = last_entry_response[2]
                services_last_status[table_name] = last_entry_status
            return jsonify(services_last_status)
        except Exception as e:
            return str(e)


if __name__ == '__main__':
   app.run(debug = True)