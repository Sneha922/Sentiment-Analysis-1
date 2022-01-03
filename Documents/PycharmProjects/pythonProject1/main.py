from tabnanny import check

from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
import sqlite3

from tweepy import cursor

from sentiment import SentimentAnalysis
import os

app = Flask(__name__,template_folder="templates")

'''app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'

conn=sqlite3.connect("Signup.db")
#c=conn.cursor()
conn.execute("CREATE TABLE signup(username TEXT, password Text, email TEXT)")
#conn.commit()
conn.close()

@app.route("/signup")
def signup():
    return render_template("Signup.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("Signup.db")
        con.row_factory=sqlite3.Row
        cur=con.execute("select * from signup where name=? and mail=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("Signup")
        else:
            flash ("Username and Password Mismatch","danger")
            return redirect (url_for("Signup"))

    @app.route('/login',methods=["GET","POST"])
    def login():
        return render_template('/login')

    @app.route('/login',methods=['GET','POST'])
    def signup(username=None):
        if request.method=='POST':
            try:
                name=request.form['username']
                password=request.form['password']
                mail=request.form['mail']
                con=sqlite3.connect("Signup.db")
                cur=con.cursor()
                cur.execute("insert into signup(username, password, mail)values(?,?,?)",(username,password,mail))
                con.commit()
                flash("Record Added Successfully","success")
            except:
                flash("Error in insert operation","danger")
            finally:
                return redirect(url_for("Signup"))
            con.close()

            return render_template('/Signup')
        @app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for("/login"))'''



'''
# initailizing the user cookie
app.secret_key = os.urandom(24)


# establishing a connection with mysql database made in xampp
try:
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="users")
    cursor = conn.cursor()
except:
   print("An exception occured")


# call the login template when the url is http://localhost:5000/

@app.route('/')
def mainp():
    return render_template('Mainpage.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('Login.html')

#@app.route('/register')
#def register():
    #return render_template('Signup.html')

@app.route('/help')
def help():
    return render_template('Contactus.html')

#call the register template when the url is http://localhost:5000/register
@app.route('/Signup')
def register():
    return render_template('Signup.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute(
       """SELECT * from `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    #check if a user has already logged in
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user(conn=None):
    #get user login data and pass the data to database
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`name`,`email`,`password`) VALUES ('{}','{}','{}')""".format(
       name, email, password))
    conn.commit()
    cursor.execute(
       """SELECT * from `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    #close the session
    session.pop('user_id')
    return redirect('/')
#here
'''
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def mainp():
    return render_template('Mainpage.html')

@app.route('/login',methods=["GET","POST"])
def login():
    return render_template('Login.html')

@app.route('/register')
def register():
    return render_template('Signup.html')

@app.route('/help')
def help():
    return render_template('Contactus.html')

@app.route('/sentiment_analyzer', methods=['POST', 'GET'])
def sentiment_analyzer():
    return render_template('sentiment_analyzer.html')

@app.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    # get user input of keyword to search and number of tweets from html form.
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    sa = SentimentAnalysis()


    # set variables which can be used in the jinja supported html page
    polarity, htmlpolarity, happy, fear, sad, neutral, keyword1, tweet1, imageid = sa.DownloadData(
        keyword, tweets)
    return render_template('result.html', polarity=polarity, htmlpolarity=htmlpolarity, happy=happy,
                           fear=fear, sad=sad,
                           neutral=neutral, keyword=keyword1, tweets=tweet1, imageid=imageid)

if __name__ == "__main__":
    app.run(debug=True)

