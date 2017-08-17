from flask import Flask, render_template, request, jsonify,redirect,url_for
from flask_login import LoginManager, current_user, login_required,logout_user, login_user
from dbhelper import DBHelper
from user import User
from passwordhelper import PasswordHelper
from forms import RegistrationForm, LoginForm
import dbsetup

app = Flask(__name__)
app.secret_key = 'tPXJY3X37QybXykV+hO-yUxsuJjfdcydcJUegjeFgMY8upz+fGs'
login_manager = LoginManager(app)
db = DBHelper()
PH = PasswordHelper()

tasks = []
completed = []
task_count = 0
c_task_count = 0
colors = ['blue', 'red', 'green', 'yellow', 'purple', 'silver']
c_tasks = []

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    form = RegistrationForm()
    return render_template('registration.html', registrationform = form)

@app.route('/login')
def log_in():
    form = LoginForm()
    return render_template('login.html', loginform = form)


@app.route("/register", methods=['GET', "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if db.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('registration.html', registrationform = form)
        salt = str(PH.get_salt())
        hashed = PH.get_hash((form.password2.data + salt).encode('utf-8'))
        db.add_user(form.email.data, salt, hashed)
        user = User(form.email.data)
        login_user(user, remember=True)
        return redirect(url_for("index"))
    return render_template('registration.html', registrationform = form)

@app.route("/loginx", methods=["GET", "POST"])
def login():
    global user
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            stored_user = db.get_user(email)
            if  not stored_user:
                form.email.errors.append("No registerd account for this email")
                
            if  stored_user and not PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
                form.password.errors.append("Incorrect password.")

            if  stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
                user = User(email)
                login_user(user, remember=True)
                return redirect(url_for('index'))
        return render_template('login.html', loginform = form)
    return redirect(url_for("home")) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    user_password = db.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route('/my-TODO', methods=['GET', 'POST'])
@login_required
def index():

    if request.method == 'POST':
        global tasks
        global task_count
        global colors
        global c_tasks
        global c_task_count
        taskx = request.form.get("task")

        if taskx:
            if taskx.strip():
                db.add_task(taskx.strip(), current_user.get_id())
    tasks = db.get_all_tasks(current_user.get_id())
    task_count = db.task_count(current_user.get_id())
    c_tasks = db.get_completed_tasks(current_user.get_id())
    c_task_count = db.c_task_count(current_user.get_id())
    user = str(current_user.get_id())
    user = user[0:user.index('@')]
    
    return render_template('index.html',tasks= tasks, colors = colors, task_count = task_count, c_tasks = c_tasks, c_task_count = c_task_count, user_name = user)

@app.route('/add_task')
@login_required
def add_task():
    try:
        desc = request.args.get('description', 0, type=str)
        global db
        global tasks
        global task_count
        global c_tasks

        db.add_task(desc, current_user.get_id())
        tasks = db.get_all_tasks(current_user.get_id())
        task_count = db.task_count(current_user.get_id())
        c_tasks = db.get_completed_tasks(current_user.get_id())
        c_task_count = db.c_task_count(current_user.get_id())
        return jsonify(count=task_count,  c_task_count = c_task_count)
    except Exception as e:
        return str(e)

@app.route('/undo')
@login_required
def undo():
    try:
        desc = request.args.get('description', 0, type=str)
        global db
        global tasks
        global task_count
        global c_tasks

        db.delete_task(desc, current_user.get_id())
        db.add_task(desc, current_user.get_id())
        tasks = db.get_all_tasks(current_user.get_id())
        task_count = db.task_count(current_user.get_id())
        c_tasks = db.get_completed_tasks(current_user.get_id())
        c_task_count = db.c_task_count(current_user.get_id())
        return jsonify(count=task_count,  c_task_count = c_task_count)
    except Exception as e:
        return str(e)

@app.route('/get_color')
@login_required
def get_color():
    try:
        global task_count
        global colors
        
        color = list(reversed(colors))[task_count%6]
        return jsonify(color=color)
    except Exception as e:
        return jsonify(color = str(e))

@app.route('/delete_task')
@login_required
def delete_task():
    global db
    global tasks
    global task_count
    global c_task_count
    global c_tasks
    desc = request.args.get('description', 0, type=str)
    
    db.delete_task(desc, current_user.get_id())
    task_count = db.task_count(current_user.get_id())
    tasks = db.get_all_tasks(current_user.get_id())
    c_tasks = db.get_completed_tasks(current_user.get_id())
    c_task_count = db.c_task_count(current_user.get_id())
    return jsonify(count=task_count, c_task_count = c_task_count)

@app.route('/complete_task')
@login_required
def complete_task():
    global db
    global tasks
    global task_count
    global c_task_count
    global c_tasks
    desc = request.args.get('description', 0, type=str)
    
    db.complete_task(desc, current_user.get_id())
    task_count = db.task_count(current_user.get_id())
    tasks = db.get_all_tasks(current_user.get_id())
    c_tasks = db.get_completed_tasks(current_user.get_id())
    c_task_count = db.c_task_count(current_user.get_id())
    return jsonify(count=task_count, c_task_count = c_task_count)
    
    

if __name__ == '__main__':
    app.run()


