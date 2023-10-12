#imports
from flask import Blueprint, render_template,url_for,request,redirect,flash
from flask_login import login_user, current_user, login_required
import sqlite3 as sql
from passlib.hash import sha256_crypt
import random
import string
import smtplib
from email.mime.text import MIMEText
###################################################################################

auth_bp=Blueprint('auth',__name__)




@auth_bp.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':

        try:
            fullname=request.form.get('fullname')
            username=request.form.get('username')
            email=request.form.get('email')
            number=request.form.get('number')
            password=request.form.get('password')
            confirmedpassword=request.form.get('confirmedpassword')
            gender=request.form.get('gender')

            print ("gender=", gender)

                
            with sql.connect("database.db") as conn:
                print ("Opened database successfully")
                
                cur = conn.cursor()
                user=cur.execute("SELECT * FROM user WHERE email=?",(email,)).fetchone()
                if user:
                    flash('Email already exists.', category='error')
                elif len(fullname) < 2 or len(username)<2:
                    flash('name must be greater than 1 character.', category='error')
                elif '@' not in email:    
                    flash('Please enter valid mail.', category='error')
                elif len(password) < 6:
                    flash('Password must be at least 7 characters.', category='error')
                elif  password != confirmedpassword:
                    flash('Passwords don\'t match.', category='error')
                elif gender is None:
                    flash('Please select your gender.', category='error')   
                else:                  
                    cur.execute("""INSERT INTO user (fullname,username,email,phone_number,pass,gender)
                                VALUES (?,?,?,?,?,?)""",(fullname,username,email,number,sha256_crypt.encrypt(password),gender))
                    print (fullname,username,email,number,password,confirmedpassword,gender)
                    return redirect(url_for('auth.login'))
                conn.commit()
                
        except Exception as e:
            conn.rollback()
            print("insertion err:"+str(e))
            
                
        conn.close()

    return render_template('signup.html')
           



@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        try:
            flag=False
            email=request.form.get('email')
            password=request.form.get('password')
            remember_me = request.form.get('remember_me')  # Added line to check "Remember Me" checkbox

            print(email,password)
            with sql.connect("database.db") as conn:
                        print ("Opened database successfully")
                        
                        cur = conn.cursor()
                        print ("cur")
                        user=cur.execute("SELECT * FROM user WHERE email=?",(email,)).fetchone()
                        print ("cur2")
                        
                        if '@' not in email:
                            flash('please enter correct mail',category='error')
                        elif not user :
                            flash('User not found',category='error')
                        elif not sha256_crypt.verify(password,user[6]):
                            flash('Please enter correct password',category='error')  
                        else:
                            return redirect(url_for('main.todolist_form'))
                            

                       
        except Exception as e:
            print("login err:"+e)
                    
        conn.close() 

    return render_template('login.html')
    



@auth_bp.route('/logout')
def logout():
    return render_template('login.html')



def generate_temporary_password():
    # Generate a random password, e.g., 12 characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def send_email(to_email, subject, message):
    # Replace this with your email sending code
    # This example uses a simple SMTP setup
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ranagaber810@gmail.com'
    smtp_password = 'dhbp xykn awjw kgbg'


    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'ranagaber810@gmail.com'
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail('ranagaber810@gmail.com', [to_email], msg.as_string())
    except Exception as e:
        print(f"Email sending error: {str(e)}")

@auth_bp.route('/reset', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'POST':
        email = request.form['email']
        
        with sql.connect("database.db") as conn:
                print ("Opened database successfully")
                
                cur = conn.cursor()
                user=cur.execute("SELECT * FROM user WHERE email=?",(email,)).fetchone()
                if user:
                        temporary_password = generate_temporary_password()
                        cur.execute("UPDATE user SET pass = ? WHERE email = ?",(sha256_crypt.encrypt(temporary_password),email))
                        print (email)
                        send_email(email, "Password Reset", f"Your temporary password is: {temporary_password}")
                        return redirect(url_for('auth.login'))
                else:
                    return "User not found."
                conn.commit()
    return render_template('reset_pass.html')