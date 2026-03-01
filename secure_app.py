from flask import Flask, render_template_string, redirect, url_for, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

csrf = CSRFProtect(app)

users = []

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Flask App</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 40px; }
        .card { background: white; padding: 20px; border-radius: 10px; width: 400px; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { padding: 8px 12px; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>

<h1> Secure Flask Application (CSRF Protected)</h1>

{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for msg in messages %}
      <p class="success">{{ msg }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}

<div class="card">
<h3>Register</h3>
<form method="POST" action="/register">
    {{ register_form.hidden_tag() }}
    {{ register_form.username.label }} {{ register_form.username() }}
    {{ register_form.password.label }} {{ register_form.password() }}
    {{ register_form.submit() }}
</form>
</div>

<div class="card">
<h3>Login</h3>
<form method="POST" action="/login">
    {{ login_form.hidden_tag() }}
    {{ login_form.username.label }} {{ login_form.username() }}
    {{ login_form.password.label }} {{ login_form.password() }}
    {{ login_form.submit() }}
</form>
</div>

<div class="card">
<h3>Send Message</h3>
<form method="POST" action="/message">
    {{ message_form.hidden_tag() }}
    {{ message_form.message.label }} {{ message_form.message() }}
    {{ message_form.submit() }}
</form>
</div>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(
        HTML,
        register_form=RegisterForm(),
        login_form=LoginForm(),
        message_form=MessageForm()
    )

@app.route("/register", methods=["POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users.append(form.username.data)
        flash("User registered successfully!")
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data in users:
            flash("Login successful!")
        else:
            flash("User not found!")
    return redirect(url_for("index"))

@app.route("/message", methods=["POST"])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        flash("Message sent successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)