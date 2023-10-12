print("hhhhh")
from flask import Blueprint, render_template, url_for,request,redirect

import sqlite3 as sql

################################################################

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
def index():
    return render_template('signup.html')



@main_bp.route('/todolist',methods=['POST'])
def todolist_form():

    try:
        todo=request.form.get('to-do')
        print(todo)
        with sql.connect("database.db") as conn:
            print ("Opened database successfully")
            
            cur = conn.cursor() 
            if(todo != None):              
                cur.execute("""INSERT INTO TODO (todo)
                            VALUES (?)""",(todo,))
            print ("after db: "+todo)
            conn.commit()
            

    
    except Exception as e:
        conn.rollback()
        print("todo: "+str(e))
    conn.close()
    

    return redirect(url_for("main.todolist_show"))



@main_bp.route('/todolist',methods=['GET'])
def todolist_show():   
    try:
        with sql.connect("database.db") as conn:
                print ("Opened database successfully")
                
                cur = conn.cursor()                  
                
                sorted_todolist= cur.execute("""
                            SELECT todo FROM TODO ORDER BY id DESC""").fetchall()
                print(sorted_todolist)   
                conn.commit()
    
    except Exception as e:
        print("todo: "+str(e))
    conn.close()


    return render_template('todo.html',todolist=sorted_todolist)


