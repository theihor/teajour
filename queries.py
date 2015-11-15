#!/usr/bin/python
import MySQLdb
from MySQLdb.cursors import DictCursor

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="12", # your password
                     db="teajourdb",# name of the data base
                     charset='utf8',
                     use_unicode=True,
                     cursorclass=DictCursor
                     )


def check_login(uname, password):
    c = db.cursor()
    c.execute("""SELECT user_kind FROM users
             WHERE user_name=%s and user_password=%s""", (uname, password))
    res = c.fetchone()
    print(res)
    if res: return res['user_kind']


def make_student_table(dicts):
    res = []
    header_set = set()
    subject_set = set()
    marks = {}
    for d in dicts:
        desc = d['description']
        if not desc:
            desc = str(d['date'])
        header_set.add(desc)
        sub = d['class_full_name']
        subject_set.add(sub)
        marks[sub] = {desc: d['mark']}

    header = [u'Предмет'] + sorted(list(header_set))
    subjects = sorted(list(subject_set))
    res.append(header)
    for sub in subjects:
        row = [sub]
        for col in header[1:]:
            if col in marks[sub]:
                row.append(marks[sub][col])
            else:
                row.append("")
        res.append(row)
    return res


def student_marks(uname):
    c = db.cursor()
    c.execute("""SELECT user_id FROM users WHERE user_name=%s and user_kind='student' """, (uname,))
    user_id = c.fetchone()['user_id']
    print(user_id)
    q = "select c.class_full_name, m.date, m.description, m.mark "
    q += "from classes as c inner join marks as m "
    q += "on c.class_id = m.class_id where m.student_id = %s"
    c.execute(q, (user_id,))

    res = c.fetchall()
    print(res)

    return make_student_table(res)


def make_teacher_table(dicts):
    res = []
    header_set = set()
    student_set = set()
    marks = {}
    for d in dicts:
        desc = d['description']
        if not desc:
            desc = str(d['date'])
        header_set.add(desc)
        student = d['surname']
        student += " " + d['name'][:1] + "."
        student += " " + d['second_name'][:1] + "."
        student_set.add(student)
        marks[student] = {desc: d['mark']}

    header = [u'Студент'] + sorted(list(header_set))
    students = sorted(list(student_set))
    res.append(header)
    for sub in students:
        row = [sub]
        for col in header[1:]:
            if col in marks[sub]:
                row.append(marks[sub][col])
            else:
                row.append("")
        res.append(row)
    return res


def teacher_table(uname, class_id=None):
    c = db.cursor()
    c.execute("""SELECT user_id FROM users WHERE user_name=%s and user_kind='teacher' """, (uname,))
    user_id = c.fetchone()['user_id']
    print(user_id)
    if not class_id:
        q = "select class_id from classes where teacher_id=%s"
        c.execute(q, (user_id,))
        class_id = c.fetchone()['class_id']
    q = "select s.name, s.second_name, s.surname, m.date, m.description, m.mark "
    q += "from students as s inner join marks as m "
    q += "on s.user_id = m.student_id where m.class_id = %s"
    c.execute(q, (class_id,))

    res = c.fetchall()
    print(res)

    return make_teacher_table(res)