# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re,datetime


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'helloHEMLO234@'
app.config['MYSQL_DB'] = 'blog'

mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('mainpage.html')
@app.route('/add')
def add():
	return render_template("add.html")

@app.route('/postblog',methods=['POST','GET'])
def postblog():
	try:
		if request.method == 'POST' and 'blog_title' in request.form and 'blog_content' in request.form:
			title = request.form['blog_title']
			content = request.form['blog_content']
			time = datetime.datetime.now()
			if not title or not content:
				raise Exception 
			cur = mysql.connection.cursor()
			cur.execute('INSERT INTO blogdetails  VALUES (NULL,%s,%s,%s,%s)',(title,content,time,session['id'],))
			mysql.connection.commit()
			cur.close()
		return redirect(url_for('add'))
	except Exception as e:
		return "error"

@app.route('/showall',methods=['GET','POST'])
def showall():
	try:
		cur=mysql.connection.cursor()
		cur.execute('select blog_title,blog_content,username,blog_id from blogdetails as b inner join accounts as a on a.id=b.id where a.id=%s',str(session['id']))
		allblog=cur.fetchall()
		cur.close()
		return render_template("showall.html",allblogs=allblog)
	except Exception as e:
		print(e)
		return "none"

@app.route('/showallblog',methods=['GET','POST'])
def showallblog():
	try:
		cur=mysql.connection.cursor()
		cur.execute('select blog_title,blog_content,username,blog_id from blogdetails as b inner join accounts as a on a.id=b.id')
		allblog=cur.fetchall()
		cur.close()
		return render_template("showallblog.html",allblogs=allblog)
	except Exception as e:
		print(e)
		return "none"

@app.route('/edit/<id>',methods=['POST','GET'])
def edit(id):
	try:
		cur=mysql.connection.cursor()
		cur.execute('select blog_title,blog_content from blogDetails where blog_id =%s',(id,))
		blog = cur.fetchone()
		cur.close()
		return render_template('edit.html',id=id,blog=blog)
	except Exception as e:
		return "error"

@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
	try:
		if not request.form['title'] or not request.form['content']:
			raise Exception 
		cur=mysql.connection.cursor()
		cur.execute('update blogDetails set blog_title=%s , blog_content=%s where blog_id =%s',(request.form['title'],request.form['content'],id))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('showall'))
	except Exception as e:
		print(e)
		return "failed"
@app.route('/delete/<id>',methods=['POST','GET'])
def delete(id):
	try:
		print(id)
		cur=mysql.connection.cursor()
		cur.execute('delete from blogDetails where blog_id =%s',(id,))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('showall'))
	except Exception as e:
		print(e)
		return "none"

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM accounts WHERE username =%s AND password =%s', (username, password))
		account = cursor.fetchone()
		cursor.close()
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			msg = 'Login success'
			return redirect(url_for('add'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			cursor.close()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

app.run(debug=True)