from flask import Flask
from flask import Blueprint, render_template, url_for
from main import main_bp
from auth import auth_bp
import sqlite3

#########################################################

conn = sqlite3.connect('database.db')
print ("Opened database successfully")
cur = conn.cursor()
with open('schema.sql') as f:
    cur.executescript(f.read())
 
print ("Table created successfully")
conn.commit()
conn.close()
###########################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
  


print("hhhhh")


################################################################

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)


