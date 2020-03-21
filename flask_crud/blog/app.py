from flask import Flask,render_template,url_for,redirect,request,session,flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
Bootstrap(app)
mysql = MySQL(app)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_blog = cur.execute("SELECT * FROM blog")
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>')
def blogs(id):
    return render_template('blogs.html',blog_id=id)

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        user_details = request.form
        if user_details['password'] != user_details['confirm_password']:
            flash('Passwords do not match! Please try again.','danger')
            return render_template('register.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(first_name,last_name,username,email,password)"\
                    "VALUES(%s,%s,%s,%s,%s)",(user_details['first_name'],user_details['last_name'],\
                        user_details['username'],user_details['email'],generate_password_hash(user_details['password'])))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login','success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        user_details = request.form
        username = user_details['username']
        cur = mysql.connection.cursor()
        user_db = cur.execute("SELECT * FROM user WHERE username=%s",([username]))
        if user_db > 0:
            user = cur.fetchone()
            if check_password_hash(user['password'],user_details['password']):
                session['login'] = True
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                flash(f"Welcome {session['first_name']}, you have been successfully logged in !",'success')
            else:
                cur.close()
                flash("Passwords do not match.",'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('Username not found.','danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/write-blog',methods=["GET","POST"])
def write_blog():
    if request.method == "POST":
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = f"{session['first_name']}+{session['last_name']}"
        session['created_on'] = datetime.utcnow()
        cur = mysql.connection.cursor()
        print(session['created_on'])
        cur.execute("INSERT INTO blog(title,body,author,created_on)"\
                    "VALUES (%s,%s,%s,%s)",(title,body,author,session['created_on']))
        mysql.connection.commit()
        cur.close()
        flash("Successfully posted new blog","success")
        return redirect('/')
    return render_template('write-blog.html')

@app.route('/my-blogs')
def my_blogs():
    return render_template('my-blogs.html')

@app.route('/edit-blog/<int:id>',methods=["GET","POST"])
def edit_blog():
    return render_template('edit-blog.html')

@app.route('/delete-blog/<int:id>',methods=["POST"])
def delete_blog(id):
    return "Successfully deleted"

@app.route('/logout')
def logout():
    return render_template('logout.html')


if __name__=='__main__':
    app.run()