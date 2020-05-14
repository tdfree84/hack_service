# hack_service
Hackable CTF style service for Computer Security at BVU 2020.

### The hack
The story is a developer accidently included the passwords with the usernames when a client runs a search. Therefore, being able to see passwords in plain text, you would want to find the admin password. 
<br/> **To do this:**
1. Register
1. Search for yourself in search bar
1. Perform a SQL injection of `ANYTHING' or '1' = '1`
1. Find the admin password on the page
1. Logout
1. Login as admin
1. Click FLAG ME
<br/>

The query hacked is `SELECT username, password FROM customers WHERE username = ' + user_input + ';`
<br/>
Certainly, the `user_input` being injected right into the query is trouble some. This is injection is not found in the registration or sign in.
