from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from google.auth import identity_toolkit
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# Get environment variables from
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')

# Construct the MySQL URI
mysql_uri = f"mysql://{db_username}:{db_password}@{db_host}/{db_name}"


app = Flask(__name__)

# Configure the Flask app
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy instance
db = SQLAlchemy(app)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)  # Assuming description can be null
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.task_name

db.create_all()

google_api_token = os.getenv("GOOGLE_API_TOKEN")


# Configure GCP API key
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

client = identity_toolkit.Client(api_key=google_api_token)

def verify_id_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = request.headers.get('Authorization')
        if id_token:
            try:
                # Verify the ID token
                decoded_token = client.verify_id_token(id_token)
                # You can access the user's email and other claims from the decoded token
                email = decoded_token['email']
                # Perform additional validation if needed
                # Load the user from the database based on the email or other claims
                user = User.query.filter_by(email=email).first()
                if user:
                    # Set the current user
                    login_user(user)
                    return f(*args, **kwargs)
            except Exception as e:
                # Handle invalid or expired ID token
                print(e)
        # Return an error response or redirect to the login page
        return redirect(url_for('login'))
    return decorated_function

@app.route('/')
@login_required
@verify_id_token
def home():
    # Display the dashboard page with an overview of tasks
    tasks = Task.query.filter_by(user_id=current_user.user_id).all()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/task', methods=['GET', 'POST'])
@login_required
@verify_id_token
def create_task():
    # Handle task creation
    if request.method == 'POST':
        task_name = request.form['task_name']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        status = "In Progress"  # Default status

        new_task = Task(task_name=task_name, description=description, due_date=due_date, priority=priority, status=status, user_id=current_user.user_id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            print(e)  # You may want to log errors in a real application
            flash("An error occurred while creating the task")

    return render_template('create_task.html')

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
@verify_id_token
def view_task(task_id):
    # Handle task viewing and updating
    task = Task.query.get(task_id)

    if task.user_id != current_user.user_id:
        flash("You don't have permission to view this task.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Assume you have form fields for task_name, description, due_date, priority, status
        task.task_name = request.form['task_name']
        task.description = request.form['description']
        task.due_date = request.form['due_date']
        task.priority = request.form['priority']
        task.status = request.form['status']

        try:
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            print(e)  # You may want to log errors in a real application
            flash("An error occurred while updating the task")

    return render_template('task_detail.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
@verify_id_token
def delete_task(task_id):
    # Handle task deletion
    task = Task.query.get(task_id)

    if task.user_id != current_user.user_id:
        flash("You don't have permission to delete this task.")
        return redirect(url_for('home'))

    try:
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        print(e)  # You may want to log errors in a real application
        flash("An error occurred while deleting the task")

    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle user registration
    return render_template('register.html')

from flask_login import login_user, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform authentication and validation
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Log in the user using Flask-Login's login_user() function
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.')

    # Render the login form
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # Log out the user using Flask-Login's logout_user() function
    logout_user()
    return redirect(url_for('login'))



@app.route('/logout')
@login_required
def logout():
    # Log out the user using Flask-Login's logout_user() function
    logout_user()
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
@verify_id_token
def settings():
    # Handle user settings
    return render_template('settings.html')

@login_manager.user_loader
def load_user(user_id):
    # Replace this with your own logic to load the user from the database based on the user_id
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)

