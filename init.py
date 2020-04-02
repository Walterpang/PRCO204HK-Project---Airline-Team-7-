from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn
import register
import login

#Define a route to hello function
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/login')
  
# Why secret_key? http://stackoverflow.com/a/22463969
app.secret_key = 'S4p9Z#Z3vjw!@J66'

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
  app.run('127.0.0.1', 5555, debug = True)