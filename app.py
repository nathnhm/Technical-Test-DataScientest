from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from src.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from src.Limiter import MyLimiter
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'usertable'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        hashedPassword = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
            name = form.name.data, 
            username = form.username.data, 
            email = form.email.data, 
            password = hashedPassword
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    else:
        return render_template('register.html', form = form)


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email = form.email.data).first()
        usersList = User.query.all()

        if user:
            if check_password_hash(user.password, form.password.data):
                session['logged_in'] = True
                session['email'] = user.email 
                session['username'] = user.username
                session['name'] = user.name
                session['usersList'] = []

                for users in usersList:
                    session['usersList'].append(users.name + ' ' + users.username)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html', form = form)


@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/test')
@MyLimiter("6/second")
def test():
    print("test")

if __name__ == '__main__':
    app.run(debug=True)