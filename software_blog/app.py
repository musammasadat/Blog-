

from flask import Flask, render_template, redirect, url_for, flash,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/new06/OneDrive/Desktop/software_blog/app.db"
app.config["SECRET_KEY"] = "my_secret_key"
db = SQLAlchemy(app)

class Logapp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(90), unique = True, nullable = False )
    email = db.Column(db.String(120))
    password = db.Column(db.String(80), nullable = False)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = Logapp(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')

        return redirect(url_for("login"))
    return render_template("register.html", form = form)


@app.route("/frontend")
def frontend():
    return render_template("frontend.html")


@app.route("/backend")
def backend():
    return render_template("backend.html")


@app.route("/fullstack")
def fullstack():
    return render_template("fullstack.html")


@app.route("/rpa")
def rpa():
    return render_template("rpa.html")

@app.route("/bilgiteknoloji")
def bilgiteknoloji():
    return render_template("bilgiteknoloji.html")


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Formdan gelen verileri alıyoruz
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')

        # Geri bildirim işleme (şu anda sadece yazdırıyoruz)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Feedback: {feedback}")
        
       
        return render_template("thank_you.html")
    

    return render_template('feedback.html')


@app.route('/thank_you')
def thank_you():
   
 print( "Geri bildiriminiz için teşekkür ederiz!")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Logapp.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash("Login Successful! ", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form = form)

    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True)