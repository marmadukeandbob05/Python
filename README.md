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
To send an email using gmail in python, use the ```send_gmail(youremail, yourpassword, to, subject, body, database)```function from easy-email, replacing youremail with your gmail account, yourpassword with your gmail password, to subject and body with their obvious values and finally replacing database with the url of your firebase realtime database or replacing it with ```None```

## For Example
```
send_gmail("johndoe@gmail.com", "password123", "email@anything.com", "This is a subject", "Hello friend, I sent this email with the easy-email module from python", "https://your-database.firebaseio.com/")
```

# Installation
Open a command window and enter the following :
```
    pip install easy-email
```
