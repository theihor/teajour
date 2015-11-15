from flask import Flask, render_template, request, redirect
from queries import *

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    password = request.form.get('password')
    print (uname, " ", password)
    user_kind = check_login(uname, password)
    print (user_kind)
    if user_kind == "admin":
        return render_template('start.html', name=uname)
    elif user_kind == "student":
        tab = student_marks(uname)
        print(tab)
        return render_template('student.html', tab=tab)
    elif user_kind == 'teacher':
        tab = teacher_table(uname)
        print(tab)
        return render_template('teacher.html', tab=tab)
    else:
        return render_template("login.html")

        
if __name__=="__main__":
    app.run()
