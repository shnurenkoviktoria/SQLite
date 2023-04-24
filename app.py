import sqlite3

import flask
from faker import Faker

fake = Faker()

try:
    con = sqlite3.connect('customers_AND_tracks.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE customers(id INTEGER ,first_name, "last_name" ,email)''')

    for i in range(100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        cur.execute(
            f"INSERT INTO customers (id, first_name, last_name, email) VALUES ({i}, '{first_name}', '{last_name}', '{email}')")

    cur.execute('''CREATE TABLE tracks(id INTEGER ,title ,artist ,length_sec INTEGER)''')

    for i in range(100):
        title = fake.text(20)
        artist = fake.name()
        length = fake.random_int(min=60, max=240)
        cur.execute(
            f"INSERT INTO tracks (id, title, artist, length_sec) VALUES ({i}, '{title}', '{artist}', {length})")

    con.commit()
    con.close()
except Exception:
    pass

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route('/names/')
def unique_names():
    con = sqlite3.connect('customers_AND_tracks.db')
    cur = con.cursor()
    unique_names_count = cur.execute("SELECT COUNT(DISTINCT first_name) FROM customers").fetchone()[0]
    con.close()

    return flask.render_template("task1.html", name=unique_names_count)


@app.route('/tracks/')
def track_count():
    con = sqlite3.connect('customers_AND_tracks.db')
    cur = con.cursor()
    track_count = cur.execute("SELECT COUNT(*) FROM tracks").fetchone()[0]
    con.close()
    return flask.render_template("task2.html", name=track_count)


@app.route('/tracks-sec/')
def track_lengths():
    con = sqlite3.connect('customers_AND_tracks.db')
    cur = con.cursor()
    tracks = cur.execute("SELECT title, length_sec FROM tracks").fetchall()
    con.close()
    return flask.render_template("task3.html", name=tracks)


if __name__ == '__main__':
    app.run()
