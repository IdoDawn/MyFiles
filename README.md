# MyFiles
to execute the task i used flask - a web application framework written in python
==

to run the website in linux environment the following commands in the terminal:
(first of all make sure you are in the project directory - cd Flask_Site)
  
# FLASK_APP=flaskwebsite.py 

# flask run --host=0.0.0.0

this might require the installation of flask beforehand
to enter the site from the broswer, use http://127.0.0.1:5000/


the home page -  will present the content of /Flask_Site/static/files, and allows you to download each one

upload file page - allows you to choose a file and store it in the files folder

register page - allows you to create an account. it stores the username and password in the database

login page - allows you to enter your existing account's details. if your input of user info exists in the database, it logs you in as a user


NOTE - the registration and storing the user data in the database works perfectly. however, the login page and code is still there, only it creates an error while submitting the form. unfortunatly i did not have the time to fix it and filter the file viewing according to the user who uploaded.
 ==
