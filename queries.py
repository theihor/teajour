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
    c.execute("""SELECT user_id, user_kind FROM users
             WHERE user_name=%s and user_password=%s""", (uname, password))
    res = c.fetchone()    
    if res: return [res['user_id'], res['user_kind']]


def make_student_table(dicts):
    res = []
    header_set = set()
    subject_set = set()
    marks = {}
    for d in dicts:
        col = d['name']
        if not col:
            col = str(d['date'])
        header_set.add(col)
        sub = d['class_full_name']
        subject_set.add(sub)
        if sub in marks:
            marks[sub][col] = d['mark']
        else:
            marks[sub] = {col: d['mark']}

    # print(marks)

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


def student_marks(user_id):
    c = db.cursor()
    # c.execute("""SELECT user_id FROM users WHERE user_name=%s and user_kind='student' """, (uname,))
    # user_id = c.fetchone()['user_id']
    # print(user_id)
    q = "select c.class_full_name, m.date, m.name, mv.mark"
    q += " from classes as c inner join marks as m on c.class_id = m.class_id"
    q += " inner join mark_values as mv on m.mark_id = mv.mark_id"
    q += " where mv.student_id = %s"
    c.execute(q, (user_id,))

    res = c.fetchall()
    # print(res)
    tab = make_student_table(res)

    q = 'select g.group_id, g.name, g.email from groups as g'
    q += ' inner join students as s on g.group_id = s.group_id'
    q += ' where s.user_id = %s'
    c.execute(q, (user_id,))
    g = c.fetchone()

    q = 'select surname, name, second_name from students where user_id=%s'
    c.execute(q, (user_id,))
    s = c.fetchone()


    return { 'table': tab,
             'student': s,
             'group': g  # contains group_id, name, email
             }


def make_teacher_table(dicts):
    res = []
    header_set = set()
    student_set = set()
    marks = {}
    for d in dicts:
        # print(d)
        desc = d['col']
        if not desc:
            desc = str(d['date'])
        header_set.add((d['mark_id'], desc))
        student = d['surname']
        student += " " + d['name'][:1] + "."
        student += " " + d['second_name'][:1] + "."
        student_set.add((d['user_id'], student))
        if not d['mark']: d['mark'] = ''
        if student in marks:
            marks[student][desc] = d['mark']
        else:
            marks[student] = {desc: d['mark']}

    columns = sorted(list(header_set), key=lambda x: x[1])
    header = [u'Студент'] + [x[1] for x in columns]
    students = sorted(list(student_set), key=lambda x: x[1])
    res.append(header)
    for s in students:
        s_name = s[1]
        row = [s_name]
        for col in header[1:]:
            if col in marks[s_name]:
                row.append(marks[s_name][col])
            else:
                row.append("")
        res.append(row)
    return {'table': res,
            'columns': columns,
            'students': students}


def teacher_table(user_id, class_id=None):
    c = db.cursor()
    # c.execute("""SELECT user_id FROM users WHERE user_name=%s and user_kind='teacher' """, (uname,))
    # user_id = c.fetchone()['user_id']
    # print(user_id)
    if not class_id:
        q = "select class_id from classes where teacher_id=%s"
        c.execute(q, (user_id,))
        class_id = c.fetchone()['class_id']
    q = "select s.user_id, s.name, s.second_name, s.surname"
    q += ", mv.mark, mv.mark_id, m.name as col, m.date"
    q += " from mark_values as mv inner join marks as m on m.mark_id = mv.mark_id"
    q += " inner join students as s on s.user_id = mv.student_id where m.class_id = %s"
    c.execute(q, (class_id,))

    res = c.fetchall()
    #print(res)

    return make_teacher_table(res)


def teacher_classes(user_id):
    c = db.cursor()
    # c.execute("""SELECT user_id FROM users WHERE user_name=%s and user_kind='teacher' """, (uname,))
    # user_id = c.fetchone()['user_id']
    # print(user_id)
    q = "select class_id, class_full_name from classes where teacher_id=%s"
    c.execute(q, (user_id,))
    dicts = c.fetchall()
    res = []
    for d in dicts:
        res.append((d['class_id'], d['class_full_name']))
    # print(res)

    return res


def set_mark(student_id, mark_id, mark):
    c = db.cursor()
    c.execute("select mark from mark_values where mark_id=%s and student_id=%s", (mark_id, student_id))
    if c.fetchone():
        c.execute("update mark_values set mark=%s where mark_id=%s and student_id=%s", (mark, mark_id, student_id))
    else:
        c.execute("insert into mark_values (student_id, mark_id, mark) values (%s, %s, %s)", (student_id, mark_id, mark))
    db.commit()


def add_mark(class_id, name=None, date=None, long_description=None):
    if not name and not date: return
    q = "INSERT INTO marks (name, date, long_description, class_id) VALUES (%s, %s, %s, %s)"
    c = db.cursor()
    c.execute(q, (name, date, long_description, class_id))
    mark_id = c.lastrowid
    q = 'select group_id from classes where class_id=%s'
    c.execute(q, (class_id,))
    group_id = c.fetchone()['group_id']
    
    q = 'select user_id as student_id from students where group_id=%s '
    c.execute(q, (group_id,))
    students = [x['student_id'] for x in c.fetchall()]
    q = 'insert into mark_values (student_id, mark_id) values (%s, %s)'
    for s_id in students:
        c.execute(q, (s_id, mark_id))
    db.commit()
