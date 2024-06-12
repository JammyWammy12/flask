from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
DATABASE = "webtags.db"


def create_connection(db_filename):
    try:
        connection = sqlite3.connect(db_filename)
        return connection

    except Error as e:
        print(e)
        return None


@app.route('/')
def render_home_page():  # put application's code here
    return render_template("index.html")


@app.route('/display/<table_type>')
def render_display_page(table_type):  # put application's code here
    query = "SELECT Tags, Description FROM web_tags WHERE type = ? "
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (table_type, ))

    data_list = cursor.fetchall()
    print(data_list)

    return render_template("display.html", data=data_list, page_title=table_type)




@app.route('/search', methods=['GET', 'POST'])
def render_search_page():
    look_up = request.form['Search']
    title = "Search for: '" + look_up + "' "
    look_up = "%" + look_up + "%"

    query = "SELECT Tags, Description FROM web_tags WHERE Tags LIKE ? OR Description LIKE ?"
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (look_up, look_up))

    data_list = cursor.fetchall()
    print(data_list)

    return render_template("display.html", data=data_list, page_title=title)


if __name__ == '__main__':
    app.run()
