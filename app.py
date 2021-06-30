from flask import Flask, render_template,url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'jajajaajajajajajajaj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email already exists')
        return redirect('/signup')
    
    new_user= User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Account not found, please try again")
        return redirect('/login')

    login_user(user, remember=remember)
    return redirect('/profile')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@login_manager.userloader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__=="__main__":
    app.run(debug=True)

