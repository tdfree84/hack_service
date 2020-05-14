from flask import abort, Flask, json, redirect,\
    render_template, request, Response, url_for, session, jsonify, make_response
import jinja2
import json
import sqlite3
from random import shuffle

app = Flask(__name__)
app.secret_key = 'hahahahhahahahahah'

@app.route('/')
def index():
    try:
        if session['logged_in']:
            pass
    except:
        return render_template('index.html', logged_in = False)

    try:
        if session['is_admin']:
            return render_template('index.html', 
                    logged_in = True,
                    is_admin = True)
    except:
        return render_template('index.html', 
                logged_in = True)

@app.route('/search_users', methods=["POST"])
def search_users():
    # Get (probably bad) username from form
    data = request.form # get data
    print(f"data {data}")
    user = data['username']

    if user == 'admin' or user == 'administrator':
        return render_template('index.html', 
                logged_in = True,
                error = 'You can\'t look up the admin.')
        

    # Horrible hacking going on here
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    script = " SELECT username, password from customers where "
    script += "username = \'" + user + "\';"
    print(f"script: {script}")
    cur.execute(script) # Terrible practice
    rows = cur.fetchall()  # Yikes
    print(f"rows queried: {rows}")
    if len(rows) == 0:
        print("sending with 0 found")
        return render_template('index.html', 
                logged_in = True,
                error = 'No users found.')
        
    r = {}
    l = []
    for row in rows:
        r = {}
        r['username'] = row[0]
        r['password'] = row[1]
        l.append(r)

    shuffle(l)

    cur.close()
    conn.close()

    return render_template('index.html', users = l, logged_in = True)


@app.route('/signin', methods=["POST"])
def signin():
    # Get username and password from form
    data = request.form # get data
    user = data['username'].lower()
    psw = data['psw'] # Bad, bad, bad

    # Get user from db if exists
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    exi = False
    cur.execute(' SELECT username, password from customers where\
            username=? ', (user, ))
    rows = cur.fetchone()
    if rows is not None:
        exi = True

    # Check if user exists
    if not exi:
        print("User [{}] doesn't exist".format(user))
        return abort(400)
    else: # They exist, check credentials
        if psw == rows[1]: # Compare passwords
            try:
                del session['is_admin']
            except:
                pass
            if user == 'admin':
                session['is_admin'] = True
            session['logged_in'] = True
            session.modified = True
            print("User [{}] signing in".format(user))
        else:
            abort(400)
    cur.close()
    conn.close()

    return 'ok'


@app.route('/signout', methods=["POST"])
def signout():
    del session['logged_in']
    session.modified = True
    return 'ok'


@app.route('/register', methods=["POST"])
def register():
    # Get user name from form to register
    data = request.form
    user = data['username'].lower()

    # Get user from db if exists
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    exi = True
    cur.execute(' SELECT username, password from customers where\
            username=? ', (user, ))
    rows = cur.fetchone()
    print("register rows",rows)
    if rows is None:
        exi = False
    
    # Check if user exists already (unique user names)
    if exi:
        print("User [{}] exists already".format(user))
        return abort(400)
    else: # User doesn't exist, register them
        psw = data['psw']
        cur.execute(' INSERT INTO customers (username, password) values \
                (?, ?)', (user, psw))
        conn.commit()
        print("User [{}] registered".format(user))

    cur.close()
    conn.close()

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=35687, debug=True)
