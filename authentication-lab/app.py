from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyD4MzuEYxNJRkfVxYeJbVKNvVIPVrHvulU",
  "authDomain": "project-8c897.firebaseapp.com",
  "projectId": "project-8c897",
  "storageBucket": "project-8c897.appspot.com",
  "messagingSenderId": "808793693155",
  "appId": "1:808793693155:web:c09a6a9a8935d406e61ed6",
  "measurementId": "G-6W3YWE6DT2",
  "databaseURL": "https://project-8c897-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'bio':bio, 'fullname':fullname, 'username':username}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        tweet = {'title':title, 'text':text, 'uid':login_session['user']['localId']}
        db.child('Users').child('UID').child('Tweets').set(tweet)
        return redirect(url_for('add_tweet'))
    else:
        return render_template("tweet.html")


if __name__ == '__main__':
    app.run(debug=True)