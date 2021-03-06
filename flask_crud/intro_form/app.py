from flask import Flask,render_template,url_for,redirect,request, session,flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os
from werkzeug.security import generate_password_hash

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

@app.route('/', methods=['GET','POST'])
def index():
    # fruits_arr=['Apple','Orange']
    # return render_template('index.html',fruits=fruits_arr)
    # return redirect(url_for('about'))
    # if request.method== 'POST':
    #     user_name = request.form.get('username')
    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO user VALUES(%s)",[user_name])
    #     mysql.connection.commit()
    #     result = cur.execute("SELECT * from user")
    #     if result > 0:
    #         users = cur.fetchall()
    #         print(users)
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cur = mysql.connection.cursor()
            name = generate_password_hash(name)
            cur.execute("INSERT INTO employee(name,age) VALUES(%s,%s)",(name,age))
            mysql.connection.commit()
            flash('Successfully inserted data!','success')
        except:
            flash('Failed to insert data','danger')
    return render_template('index.html')

@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cur.fetchall()
        # session['username'] = employees[0]['name']
        return render_template('employees.html',employees=employees)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/css')
def css():
    return render_template('css.html')

if __name__ == '__main__':
    app.run(debug=True)