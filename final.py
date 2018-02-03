"""
***************************************************************************
 * Copyright (C) 2018 Ben Sommer benrsommer@icloud.com
 *
 * This file is part of the Email Manager.
 *
 * Email Manager can not be copied and/or distributed without the express
 * permission of Ben Sommer
 **************************************************************************
 """

# imports
from tkinter import *
import hashlib
import uuid
from tkinter import messagebox
from time import sleep
import smtplib
import random
from firebase import firebase
contactlist = ["john.doe@example.com"]

# setting variables
listofcontacts = []
firebase = firebase.FirebaseApplication("https://email-database-28125.firebaseio.com/")
data = firebase.get("/contacts", None)

# defining home screen functions
def sign_up():
	adduser = (e3.get())
	addpassword = (e4.get())

	# clearing password box
	e4.delete(0, 'end')
	hashed_password = hash_password(addpassword)

	# removing special characters

	adduser = adduser.replace("@", "_A_")
	adduser = adduser.replace(".", "_D_")

	# adding user to database
	firebase.put("/user", (adduser), hashed_password)



def log_in():
	try:

		# username exists?
		replaceuser = (e1.get())
		new1 = replaceuser.replace("@", "_A_")
		new2 = new1.replace(".", "_D_")
		firebase.get("/user", (new2))


	except FileNotFoundError :
		# displaying error message
		messagebox.showinfo("Info", "No account with that username!")
	else:
		# obtaining user input
		usernameguess = (e1.get())
		passwordguess = (e2.get())
		user_attempt = usernameguess
		pwd_attempt = passwordguess



		# clearing password box
		e2.delete(0, 'end')

		# removing special characters
		user_attempt = user_attempt.replace("@", "_A_")
		user_attempt = user_attempt.replace(".", "_D_")

		username = usernameguess
		password = firebase.get("/user", (user_attempt))


		try:
			username = username.rstrip()
			password = password.rstrip()
		except AttributeError :
			messagebox.showinfo("Info", "No account with that username!")



		if username == usernameguess:

			# checking password
			if check_password(password, pwd_attempt):
				global user_at
				user_at = user_attempt
				global guser
				guser = user_attempt

				global gpass
				gpass = pwd_attempt


				def sendmail():
					try:
						boxaddress = " "
						userserver = var2.get()

						# setting appropriate address
						if userserver == "iCloud":
							boxaddress = "smtp.mail.me.com"
						if userserver == "Gmail":
							boxaddress = "smtp.gmail.com"
						if userserver == "Hotmail":
							boxaddress = "smtp.live.com"
						if userserver == "Yahoo":
							boxaddress = "smtp.mail.yahoo.com"
						if userserver == "O2":
							boxaddress = "smtp.o2.co.uk"

						# getting contents of eMail
						boxport = 25
						getTo = var.get()
						getBody = e13.get()
						finalBody = (getBody)
						subJ = (e11.get())

						# launching SMTP
						smtpObj = smtplib.SMTP(boxaddress, boxport)
						smtpObj.ehlo()
						smtpObj.starttls()

						newguser = guser.replace("_A_", "@")
						newestguser = newguser.replace("_D_", ".")



						# logging in
						smtpObj.login(str(newestguser), str(passwordguess))
						smtpObj.sendmail(str(newestguser), str(getTo), (("From:" + str(newestguser) + "\n") + ("To:" + str(getTo) + "\n") + ("Subject:" + str(subJ)) + "\n" + (finalBody)))

						smtpObj.quit()

						# sent email comfirmation
						message = ("Sent eMail to : " + str(getTo))
						messagebox.showinfo("Info", message)

						splitguser, b = user_at.split("_A_")

						complete = ["'", (subJ.title()), "'", " Sent by : ", splitguser]
						sentmessagetext = "".join(complete)
						firebase.put("/emails", sentmessagetext, finalBody)
					except smtplib.SMTPAuthenticationError:
						# checking for Authentication error
						messagebox.showinfo("Info", "Authentication error \n Check your username and password \n You may need to enable less secure apps \n you can do so at https://myaccount.google.com/lesssecureapps")



				# Mail client
				root = Tk()
				root.iconbitmap('favicon.ico')
				root.geometry("425x325")
				root.configure(background="#ff4f30")
				root.title("Emailer")

				# Writing labels
				Label(root, text="Welcome to the email client", bg="#ff4f30").grid(row=1, column=2, sticky=N+S+W+E)
				Label(root, text="To :", bg="#ff4f30").grid(row=2, column=1, sticky=N+S+W+E)
				Label(root, text="Subject :", bg="#ff4f30").grid(row=3, column=1, sticky=N+S+W+E)
				Label(root, text="Body :", bg="#ff4f30").grid(row=4, column=1, sticky=N+S+W+E)
				Label(root, text="Email Provider :", bg="#ff4f30").grid(row=5, column=1, sticky=N+S+W+E)

				# defining entry box
				e11 = Entry(root)
				e13 = Entry(root)
				e11.grid(row=3, column=2, sticky=N+S+W+E)
				e13.grid(row=4, column=2, sticky=N+S+W+E)


				# defining button
				Button(root, text='Send Email', command=sendmail).grid(row=5, column=3, sticky=W, pady=4)

				# adding top menu bar
				menubar = Menu(root)
				menubar.add_command(label="Help", command=helpuser)
				menubar.add_command(label="Contacts", command=contacts)
				menubar.add_command(label="Quit", command=root.quit)
				root.config(menu=menubar)

				# reseting choices
				contactlist = ["john.doe@example.com"]
				listofcontacts = []

				# writing contacts to string
				for item in data:
					stuff = data[item]
					stuff = stuff.replace("_A_", "@")
					stuff = stuff.replace("_D_", ".")

					contactlist.append(stuff)


				for item in contactlist:
					listofcontacts.append(item)

				# defining contact drop down menu
				var = StringVar(root)
				var.set("Select a contact")
				choices = listofcontacts
				optio = OptionMenu(root, var, *choices)
				optio.grid(row=2, column=2)

				# defining email provider drop down box
				var2 = StringVar(root)
				var2.set("Gmail")
				choices2 = ("iCloud", "Gmail", "Hotmail", "Yahoo", "O2")
				option2 = OptionMenu(root, var2, *choices2)
				option2.grid(row=5, column=2)

				# starting window
				mainloop()
			else:
				# showing incorrect password dialouge
				messagebox.showinfo("Info", "Incorrect Password")

		else:
			# showing incorrect username dialouge
			messagebox.showinfo("Info", "Incorrect Username")


def contacts():

	# defining contacts page
	base = Tk()
	base.iconbitmap('favicon.ico')
	base.geometry("410x280")
	base.configure(background="#ff4f30")
	base.title("Contacts")

	# adding text
	Label(base, text="Welcome to the contacts manager", bg="#ff4f30").grid(row=1, column=2, sticky=N+S+W+E)
	Label(base, text="Add Contact", bg="#ff4f30").grid(row=2, column=1, sticky=N+S+W+E)
	Label(base, text="Email :", bg="#ff4f30").grid(row=4, column=1, sticky=N+S+W+E)
	Label(base, text="Name :", bg="#ff4f30").grid(row=3, column=1, sticky=N+S+W+E)
	Label(base, text="Current Contacts :", bg="#ff4f30").grid(row=6, column=1, sticky=N+S+W+E)

	# defining entry boxes
	e23 = Entry(base)
	e24 = Entry(base)
	e23.grid(row=4, column=2, sticky=N+S+W+E)
	e24.grid(row=3, column=2, sticky=N+S+W+E)




	# defining what to do to add a contact
	def addcontact():
		saidname = e24.get()
		saidemail = e23.get()
		saidemail = saidemail.replace("@", "_A_")
		saidemail = saidemail.replace(".", "_D_")
		firebase.put("/contacts", saidname, saidemail)


	# defining button
	Button(base, text='Add contact', command=addcontact).grid(row=5, column=3, sticky=W, pady=4)

	# showing all contacts
	list2 = Listbox(base, height=6, selectmode="SINGLE")
	list2.grid(row=6, column=2)

	for item in data:
		smail = data[item]
		smail = smail.replace("_A_", "@")
		smail = smail.replace("_D_", ".")
		listofcontacts.append(smail)



def hash_password(password):
	# uuid is used to generate a random number
	salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
	# checking password
	password, salt = hashed_password.split(':')
	return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def helpuser():
	# once the help button is clicked
	messagebox.showinfo("Help", "To Sign Up: \n Enter a username and password and click 'Sign Up' \n To Log In: \n Enter your username and password and click 'Log In'")

# defining home page
master = Tk()

master.iconbitmap('program_icon.ico')
master.geometry("410x280")
master.configure(background="#ff4f30")
master.title("Emailer : Log In | Sign Up")

# adding text
Label(master, text="Welcome to the Emailer \n Sign up or Log in \n Note: Your password is protected by hash encryption", bg="#ff4f30").grid(row=0, column=1, sticky=N+S+W+E)
Label(master, text="Log In", bg="#ff4f30").grid(row=1, column=1, sticky=N+S+W+E)
Label(master, text="Email", bg="#ff4f30").grid(row=2, sticky=N+S+W+E)
Label(master, text="Password", bg="#ff4f30").grid(row=3, sticky=N+S+W+E)

Label(master, text="Sign Up", bg="#ff4f30").grid(row=5, column=1, sticky=N+S+W+E)
Label(master, text="Email", bg="#ff4f30").grid(row=6, sticky=N+S+W+E)
Label(master, text="Password", bg="#ff4f30").grid(row=7, sticky=N+S+W+E)

# adding top menu
menubar = Menu(master)
menubar.add_command(label="Help", command=helpuser)
menubar.add_command(label="Quit", command=master.quit)
master.config(menu=menubar)

# defining user input boxes
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)

e1.grid(row=2, column=1, sticky=N+S+W+E)
e2.grid(row=3, column=1, sticky=N+S+W+E)
e3.grid(row=6, column=1, sticky=N+S+W+E)
e4.grid(row=7, column=1, sticky=N+S+W+E)

# setting e2 and e4 to only display '*' character
e2.config(show="*")
e4.config(show="*")

# defining buttons
Button(master, text='Sign Up', command=sign_up).grid(row=8, column=2, sticky=W, pady=4)
Button(master, text='Log In', command=log_in).grid(row=4, column=2, sticky=W, pady=4)

# starting window
mainloop( )
