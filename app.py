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
    # If the user is not logged in
    try:
        if session['logged_in']:
            pass
    except:
        return render_template('index.html', logged_in = False)

    # Must be logged in, check if admin
    try:
        if session['is_admin']:
            return render_template('index.html', 
                    logged_in = True,
                    is_admin = True)
    except:
        return render_template('index.html', 
                logged_in = True)


@app.route('/flag_me', methods=["POST"])
def send_flag():
    # Must be logged in, check if admin
    try:
        if session['is_admin']:
            return 'CONGRATS, you found the flag.'
    except:
        return render_template('index.html', 
                logged_in = True)


@app.route('/search_users', methods=["POST"])
def search_users():
    '''
        This query is hackable if the user enters
        [ anything' or '1' = '1 ]
        This will query every user in the database.
        Trying to run another query will not work due to sqlite3
            error on trying to run multiple queries at once.
        The hacker then needs to find the admin password in the list.
        Using the admin's password, they must logout of current session,
            login as admin,
            click FLAGME.
    '''

    # Get (probably bad) username from form
    data = request.form # get data
    user = data['username']

    # Stop simple admin lookup by saying no to admin query
    if 'admin' in user:
        return render_template('index.html', 
                logged_in = True,
                error = 'You can\'t look up the admin.')
        

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Horrible programming practice here #
    script = " SELECT username, password from customers where "
    # Let the user's input be injected right into the query!! :((
    script += "username = \'" + user + "\';" 

    cur.execute(script) # Terrible. Run the query. Yikes
    rows = cur.fetchall()

    # If the search found nothing
    if len(rows) == 0:
        return render_template('index.html', 
                logged_in = True,
                error = 'No users found.') # Error message
        
    # Serialize the results
    l = [] # List of dictionaries
    for row in rows:
        r = {}
        r['username'] = row[0]
        r['password'] = row[1]
        l.append(r)

    shuffle(l) # Randomize the results so admin isn't at top

    cur.close()
    conn.close()

    return render_template('index.html', 
            users = l, # User list
            logged_in = True)


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
    # Securely lookup user with prepared statement
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
            # Reset admin token
            try:
                del session['is_admin']
            except:
                pass
            # Check if they are admin
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

    # Securely lookup user with prepared statement
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

        # Securely enter the new user with prepared statements
        cur.execute(' INSERT INTO customers (username, password) values \
                (?, ?)', (user, psw))
        conn.commit()
        print("User [{}] registered".format(user))

    cur.close()
    conn.close()

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=35687, debug=True)
