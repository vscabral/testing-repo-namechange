# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'database.db'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
	cur = g.db.execute('select ml, timestamp from measurements order by timestamp')
	entries = [dict(ml=row[0], timestamp=row[1]) for row in cur.fetchall()]
	return render_template('home.html', entries=entries)
	# return str(entries)

@app.route('/add', methods=['POST'])
def add_entry():
	g.db.execute("insert into measurements (ml) values (?)", [request.form['ml']])
	g.db.commit()
	return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
