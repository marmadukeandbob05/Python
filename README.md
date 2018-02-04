# Python
A collection of python related things.

# Emailer
Replace the firebase url with the url of your realtime database hosted with firebase.

Change the 'Rules' to the following :
```
    ".read": true,
    ".write": true
```
This will enable the program to write to the database.

# Easy Email Module
Use the function
```python
send_gmail(youremail, yourpassword, to, subject, body, database)
```

