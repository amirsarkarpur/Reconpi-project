from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def find_data():

    conn = sqlite3.connect('data1.db')
    cursor = conn.cursor()

    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    all_data = {}


    for table_name in tables:

        table_name = table_name[0]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        table_data = []



        for row in rows:

            row_dict = dict(zip(columns, row))
            table_data.append(row_dict)


        
        all_data[table_name] = table_data

    conn.close()
    return all_data


@app.route('/')
def index():

    data = find_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
