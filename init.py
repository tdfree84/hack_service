'''
    Sets up database for backend of hackable website.
    Adds 100 random users plus the hackable one which is
        admin [some_random_pass]
'''

import sqlite3
import random
conn = None

# Create the database
try:
    conn = sqlite3.connect('database.db')
    print("Database created...")
except:
    raise Exception("Could not create db")

# Create the table
try:
    conn.execute(' DROP TABLE if exists customers ')
    conn.execute(' CREATE TABLE customers (username TEXT, password TEXT) ')
    print("Table added...")
except:
    raise Exception("Could not create table")

MAX = 100
# Add default users to table
try:
    # Use random names and passwords for each time website is ran
    ps = [] # Collect random passwords
    with open('ps.txt', 'r') as f:
        ps = f.readlines()
    ns = [] # Collecct random names
    with open('ns.txt', 'r') as f:
        ns = f.readlines()
    ns = [x[:-1] for x in ns] # Cut off new lines
    ps = [x[:-1] for x in ps] # Cut off new lines

    extra_names = '' 
    for i in range(MAX):
        extra_names += '(\''
        extra_names += random.choice(ns)
        extra_names += '\', \''
        extra_names += random.choice(ps)
        if i == MAX-1:
            extra_names += '\')'
        else:
            extra_names += '\'), '

    # Set admin pass
    admin_pass = random.choice(ps)

    conn.execute(' INSERT INTO customers (username, password) values \
            (\'admin\', \''+admin_pass+'\'),'\
            +extra_names)

    conn.commit()
    print("Default users added")
except:
    raise Exception("Could not insert into customers")

# Query to make sure
try:
    cur = conn.cursor()
    cur.execute( ' SELECT * FROM customers ')
    rows = cur.fetchall()
    assert len(rows) == MAX+1 # Plus one for admin

except:
    raise Exception("Default users not found")

print("Success")
