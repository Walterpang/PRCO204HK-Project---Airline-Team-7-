from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

  
#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
  #grabs information from the forms
  username = request.form['username']
  password = request.form['password']
  #usrtype = request.form['usrtype']

  #cursor used to send queries
  cursor = conn.cursor()
  #executes query
  query = 'SELECT * FROM tbl_user WHERE `user_username` = %s and `user_password` = md5(%s)'

  cursor.execute(query, (username, password))
  #stores the results in a variable
  data = cursor.fetchone()
  #use fetchall() if you are expecting more than 1 data row
  cursor.close()
  error = None
  if(data):
    #creates a session for the the user
    #session is a built in
    session['username'] = username
    return redirect(url_for('index'))
    # if usrtype == 'staff':
      # return redirect(url_for('staffHome'))
    # elif usrtype == 'customer':
      # return redirect(url_for('customerHome'))
    # else:
      # return redirect(url_for('agentHome'))
    
  else:
    #returns an error message to the html page
    error = 'Invalid login or username'
    return render_template('login.html', error=error) 