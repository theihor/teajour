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


def student_marks(student_login):
    c = db.cursor()
    c.execute("""SELECT user_id FROM users WHERE user_name=%s""", (student_login,))
    user_id = c.fetchone()['user_id']
    print(user_id)
    c.execute("""SELECT student_id FROM students WHERE user_id=%s""", (user_id,))
    student_id = c.fetchone()['student_id']
    print(student_id)
    q = "select c.class_full_name, m.date, m.description, m.mark "
    q += "from classes as c inner join marks as m "
    q += "on c.class_id = m.class_id where m.student_id = %s"
    c.execute(q, (student_id,))

    res = c.fetchall()
    print(res)

    return make_student_table(res)
