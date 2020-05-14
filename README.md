# hack_service
Hackable CTF style service for Computer Security at BVU 2020.

### The hack
This service is a hack-able "banking" website. On it, there are banking tools such as a loan interest calculator, a real calculator, a stock ticker tape, and an info box about your connection. These interactive tools are just for looks. To use the website, a client can register, login, and search for users to send money to. The story is a developer accidently included the passwords with the usernames when a client runs a search. Therefore, being able to see passwords in plain text, you would want to find the admin password to get the flag in a CTF contest.
<br/> **To do this:**
1. Register
1. Search for yourself in search bar and observe the results are USER | PASSWORD
1. Perform a SQL injection of `ANYTHING' or '1' = '1`
1. Find the admin password on the page
1. Logout
1. Login as admin
1. Click FLAG ME
<br/>

The query hacked is `SELECT username, password FROM customers WHERE username = ' + user_input + ';`
<br/>
Certainly, the `user_input` being injected right into the query is troublesome. This is injection is not found in the registration or sign in.

### The flag
Currently, there is a simple response sent back to the user. The user is alerted with an alert box of the flag. To put your CTF contest's flag, use this method to set the flag -> [set flag method](https://github.com/tdfree84/hack_service/blob/d8520bb62915356077b30f5824ec0ed21d7f41f1/app.py#L32)

### Dev/Setup
Dependencies: 
* `sudo apt-get install python3 python3-pip`
* `pip3 install pipenv` <br/>


Setup:
1. `git clone https://github.com/tdfree84/hack_service.git`
1. `cd hack_service`
1. `pipenv install`
1. `pipenv shell`
1. TO RUN: `./scripts/run` [_Set port in app.py_](https://github.com/tdfree84/hack_service/blob/f70caffd0fe6dbe4c1e450022deba5549cc7aad4/app.py#L192)


### Extra
The files `ns.txt`, `ps.txt`, and `init.py` are used to setup the `sqlite3` database. `ns.txt` is filled with random names. `ps.txt` is filled with very common passwords. `init.py` uses these two files to generate _random_ users for the website. It generates 100 to be exact. The admin user is a plus one -- 101 users in total.
