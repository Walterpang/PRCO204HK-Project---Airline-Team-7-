from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/registerCustomer')
def registerCustomer():
  return render_template('registerCustomer.html')

#Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
  #grabs information from the forms
  email = request.form['inputEmail']
  name = request.form['inputName']
  password = request.form['inputPassword']
  #building_number = request.form['building_number']
  #street = request.form['street']
  ##city = request.form['city']
  #state = request.form['state']
  #phone_number = request.form['phone_number']
  #passport_number = request.form['passport_number']
  #passport_expiration = request.form['passport_expiration']
  #passport_country = request.form['passport_country']
  #date_of_birth = request.form['date_of_birth']

  #cursor used to send queries
  cursor = conn.cursor()
  #executes query
  query = "SELECT * FROM tbl_user WHERE user_email = %s "
  cursor.execute(query, email)
  #stores the results in a variable
  data = cursor.fetchone()
  #use fetchall() if you are expecting more than 1 data row
  error = None
  if(data):
    #If the previous query returns data, then user exists
    error = "This user already exists"
    return render_template('registerCustomer.html', error = error)
  else:
    ins = 'INSERT INTO tbl_user(user_email,user_username, user_password) VALUES(%s, %s, md5(%s))'
    cursor.execute(ins, (email, name, password))
	#ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
    conn.commit()
    cursor.close()
    return render_template('index.html')