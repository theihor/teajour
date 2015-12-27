from flask import Flask, render_template, request, redirect, url_for, jsonify
from queries import *

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    password = request.form.get('password')
    # print (uname, " ", password)
    user_info = check_login(uname, password)
    # print ("user_info =", user_info)
    if not(user_info):
        return render_template("login.html")
    user_kind = user_info[1]
    user_id = user_info[0]
    # print ("GELLO")
    # print ("dddd",user_kind)
    if user_kind == "admin":
        return redirect(url_for('.admin', user_id=user_id))
        # return adminpage(user_id)
    elif user_kind == "student":
        return redirect(url_for('.student', user_id=user_id))
        # return studentpage(user_id)
    elif user_kind == 'teacher':
        return redirect(url_for('.teacher', user_id=user_id))
        # return teacherpage(user_id)
    else:
        return render_template("login.html")

@app.route('/admin')
def admin():
    user_id = request.args['user_id']
    return render_adminpage(user_id)

@app.route('/student')
def student():
    user_id = request.args['user_id']
    return render_studentpage(user_id)

@app.route('/teacher')
def teacher():
    user_id = request.args['user_id']
    return render_teacherpage(user_id)

@app.route('/teacher_data', methods=['POST'])
def teacher_data():
    print("teacher_data")
    user_id = request.form.get("data")    
    teacher_c = teacher_classes(user_id)
    tab = teacher_table(user_id)
    print("TEACHER_CLASSES = ", teacher_c)
    print("TABLE = ", tab)
    return jsonify({'teacher_classes' : teacher_c, 'teacher_table' : tab})

@app.route('/update', methods=['POST'])
def updatepage():
    student_id = request.form.get('student_id')
    teacher_id = request.form.get('teacher_id')
    res = teacher_table(teacher_id)
    # print (student_id)
    # print("hello")
    return render_template("update.html", teacher_id=teacher_id, student_id=student_id, zipped=res['columns'])

@app.route('/updated', methods=['POST'])
def updated():
    # print("hello")
    mark_id = request.form.get('dates')
    mark = request.form.get('mark')
    student_id = request.form.get('student_id')
    teacher_id = request.form.get('teacher_id')
    
    if (mark == ""):
        mark = None
    # print (mark_id)
    # print (student_id)
    # print (mark)
    
    set_mark(student_id, mark_id, mark)
    return redirect(url_for('.teacher', user_id=teacher_id))

@app.route('/add', methods=['POST'])
def addpage():
    # print("hello1")
    class_id = request.form.get('class_id')
    # print("hello2")
    teacher_id = request.form.get('teacher_id')
    # print (teacher_id)
    # print("hello")
    return render_template("add.html", teacher_id=teacher_id, class_id=class_id)

@app.route('/added', methods=['POST'])
def addedpage():
    class_id = request.form.get('class_id')
    # print (class_id)
    teacher_id = request.form.get('teacher_id')
    # print (teacher_id)
    name = request.form.get('name')
    # print (name)
    date = request.form.get('date')
    # print (date)
    description = request.form.get('description')
    # print ("descrip =",description)
    if (name == "" and date == ""):
        return "Введіть дату або назву"
    if (name == ""):
        name = None
    if (date == ""):
        date = None
    if (description == ""):
        description = None
    # print (teacher_id)
    # print("hello")
    add_mark(class_id, name, date, description)
    return redirect(url_for('.teacher', user_id=teacher_id))

    
def render_adminpage(user_id):
    return render_template('start.html', name=user_id)
    
def render_studentpage(user_id):
    tab = student_marks(user_id)
    # print(tab)
    student_name =tab['student']['surname'] + " " + tab['student']['name'] + " " + tab['student']['second_name']
    return render_template('student.html',student_name=student_name, group=tab['group']['name'], tab=tab['table'])

def render_teacherpage(user_id):
    # print("Hi there", user_id)
    teacher_c = teacher_classes(user_id)
    # print(teacher_c)
    tab = teacher_table(user_id)
    # print("tab =", tab)
    # print("1 = ",tab["table"][0])
    # print("2 = ", tab['columns'])
    
    return render_template('teacher.html', teacher_id=user_id, hzipped=zip(tab["table"][0][1:], tab['columns']), bzipped=zip(tab['table'][1:],tab['students']), teacher_classes=teacher_c)
        
if __name__=="__main__":
    app.run()
