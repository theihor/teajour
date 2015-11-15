from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def check_login(uname, password):
    if (uname and password):
        return True
    else:
        return False

@app.route('/')
def homepage():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    password = request.form.get('password')
    print (uname, " ", password)
    print (check_login(uname, password))
    my_list=[{'sub':"math", 'mark':5},{'sub':"history", 'mark':5}]
    print (my_list)
    return render_template('student.html', my_list=my_list)

        
if __name__=="__main__":
    app.run()
