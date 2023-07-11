## ----- IMPORTS STARTS ----- ##
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, flash, url_for, send_from_directory
import os
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import pycountry
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# import random
# import time
# from sqlalchemy import inspect
# from flask import jsonify
# import json


## ----- IMPORT ENDS ----- ##





## ----- CONFIGURATIONS STARTS ----- ##

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

load_dotenv()  # Load environment variables from .env file

#secret key
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


#file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# email connection
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")

admin_email = os.getenv('ADMIN_EMAIL')
admin_password = os.getenv('ADMIN_PASSWORD')

mail = Mail(app)
recipient = os.environ.get("MAIL_USERNAME")




## ----- CONFIGURATIONS ENDS ----- ##





## ----- DATABASE STARTS ----- ##


registration_table = db.Table(
    'registration',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    eligibility = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)
    course_content = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    deadline_date = db.Column(db.Date, nullable=True)
    quizzes = db.relationship('Quiz', backref='course', lazy=True)
    applications = db.relationship('Application', backref='course', lazy='dynamic', cascade='all, delete-orphan')

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    registered_courses = db.relationship('Course', secondary=registration_table, backref=db.backref('registered_users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref='applications')
    status = db.Column(db.String(20), nullable=False)


## ----- DATABASE ENDS ----- ##




## ----- ROUTES STARTS  ----- ##


@app.route('/')
def index():
    courses = Course.query.all()
    blogs = Blog.query.all()
    return render_template('index.html', courses=courses, blogs=blogs)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/submitForm', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')


    msg = Message('New Form Submission', sender=email, recipients=[recipient])
    msg.body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

    mail.send(msg)

    return render_template('success.html', name=name)



@app.route('/courses')
def courses_page():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@app.route('/blogs')
def blogs_page():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        country = request.form['country']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        gender = request.form['gender']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect('/register')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect('/login')

        new_user = User(first_name=first_name, last_name=last_name, email=email, country=country, dob=dob, gender=gender)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # Automatically log in the user
        flash('Account created successfully!', 'success')
        return redirect('/dashboard')

    countries = list(pycountry.countries)
    return render_template('register.html', countries=countries)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect('/login')

        login_user(user)  # Log in the user
        return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    registered_courses = user.registered_courses
    applications = user.applications

    # Check if the application deadline has passed and update the status accordingly
    for application in applications:
        if application.course.deadline_date < datetime.now().date():
            application.status = 'Cancelled'
    db.session.commit()

    return render_template('user_dashboard.html', user=user, registered_courses=registered_courses, applications=applications, datetime=datetime)




@app.route('/user-logout')
@login_required
def user_logout():
    logout_user()  # Log out the user using Flask-Login
    flash('You have been logged out.', 'success')
    return redirect('/login')




@app.route('/terms')
def terms_page():
    return render_template('terms.html')


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
        if email == admin_email and password == admin_password:
            session['admin'] = True
            return redirect('/admin-dashboard')
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' in session:
        email = admin_email   
        return render_template('admin_dashboard.html', email=email)
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/add-course', methods=['GET', 'POST'])
def add_course():
    if 'admin' in session:
        if request.method == 'POST':
            title = request.form['title']
            cost = request.form['cost']
            eligibility = request.form['eligibility']
            duration = request.form['duration']
            slug = request.form['slug']
            course_content = request.form['course_content']
            start_date = request.form['start_date'] 
            deadline_date = request.form['deadline_date']  


            # Handle file upload
            cover_photo = request.files['cover_photo']
            if cover_photo.filename != '' and allowed_file(cover_photo.filename):
                filename = secure_filename(cover_photo.filename)
                cover_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_photo_path = filename  # Save only the filename without the folder path
            else:
                cover_photo_path = None

            course = Course(title=title, cost=cost, eligibility=eligibility, duration=duration,
                            slug=slug, cover_photo=cover_photo_path, course_content=course_content, start_date=start_date, deadline_date=deadline_date)
            db.session.add(course)
            db.session.commit()

            flash('Course added successfully.', 'success')
            return redirect('/admin-dashboard')

        return render_template('add_course.html')
    else:
        return redirect('/admin-login')




@app.route('/admin-dashboard/edit-courses')
def edit_courses():
    if 'admin' in session:
        courses = Course.query.all()
        return render_template('edit_courses.html', courses=courses)
    else:
        return redirect('/admin-login')

@app.route('/admin-dashboard/edit-course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if 'admin' in session:
        course = Course.query.get(course_id)

        if request.method == 'POST':
            # Update the course details
            course.title = request.form['title']
            course.cost = request.form['cost']
            course.eligibility = request.form['eligibility']
            course.duration = request.form['duration']
            course.slug = request.form['slug']
            course.course_content = request.form['course_content']
            course.start_date = request.form['start_date']  
            course.deadline_date = request.form['deadline_date']

            # Check if a new cover photo was uploaded
            if 'cover_photo' in request.files:
                cover_photo = request.files['cover_photo']
                if cover_photo and allowed_file(cover_photo.filename):
                    # Save the uploaded cover photo to a designated folder
                    filename = secure_filename(cover_photo.filename)
                    cover_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # Update the course's cover photo path
                    course.cover_photo = filename

            db.session.commit()

            flash('Course updated successfully!', 'success')
            return redirect('/admin-dashboard/edit-courses')

        return render_template('edit_course.html', course=course)
    else:
        return redirect('/admin-login')




@app.route('/admin-dashboard/delete-course/<int:course_id>', methods=['GET'])
def delete_course(course_id):
    if 'admin' in session:
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            flash('Course deleted successfully!', 'success')
            # Redirect to the edit-courses page with the deleted_course_id query parameter
            return redirect(url_for('edit_courses', deleted_course_id=course_id))
        else:
            flash('Course not found.', 'error')

        return redirect('/admin-dashboard/edit-courses')
    else:
        return redirect('/admin-login')



@app.route('/admin-dashboard/add-blog', methods=['GET', 'POST'])
def add_blog():
    if 'admin' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            slug = request.form['slug']
            duration = request.form['duration']
            content = request.form['content']

            # Handle file upload
            cover_photo = request.files['cover_photo']
            if cover_photo.filename != '' and allowed_file(cover_photo.filename):
                filename = secure_filename(cover_photo.filename)
                cover_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cover_photo_path = filename  # Save only the filename without the folder path
            else:
                cover_photo_path = None

            blog = Blog(title=title, author=author, slug=slug, duration=duration,
                        cover_photo=cover_photo_path, content=content)
            db.session.add(blog)
            db.session.commit()

            flash('Blog added successfully.', 'success')
            return redirect('/admin-dashboard')

        return render_template('add_blog.html')
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/edit-blogs')
def edit_blogs():
    if 'admin' in session:
        blogs = Blog.query.all()
        return render_template('edit_blogs.html', blogs=blogs)
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/edit-blog/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id):
    if 'admin' in session:
        blog = Blog.query.get(blog_id)

        if request.method == 'POST':
            # Update the blog details
            blog.title = request.form['title']
            blog.author = request.form['author']
            blog.slug = request.form['slug']
            blog.duration = request.form['duration']
            blog.content = request.form['content']

            # Check if a new cover photo was uploaded
            if 'cover_photo' in request.files:
                cover_photo = request.files['cover_photo']
                if cover_photo and allowed_file(cover_photo.filename):
                    # Save the uploaded cover photo to a designated folder
                    filename = secure_filename(cover_photo.filename)
                    cover_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # Update the blog's cover photo path
                    blog.cover_photo = filename

            db.session.commit()

            flash('Blog updated successfully!', 'success')
            return redirect('/admin-dashboard/edit-blogs')

        return render_template('edit_blog.html', blog=blog)
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/delete-blog/<int:blog_id>', methods=['GET'])
def delete_blog(blog_id):
    if 'admin' in session:
        blog = Blog.query.get(blog_id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            flash('Blog deleted successfully!', 'success')
            # Redirect to the edit-blogs page with the deleted_blog_id query parameter
            return redirect(url_for('edit_blogs', deleted_blog_id=blog_id))
        else:
            flash('Blog not found.', 'error')

        return redirect('/admin-dashboard/edit-blogs')
    else:
        return redirect('/admin-login')




@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return {'error': 'No file selected'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Return the uploaded image URL in the JSON response
        return {'location': url_for('uploaded_image', filename=filename)}

    return {'error': 'Invalid file'}, 400



@app.route('/uploads/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/blog/<slug>')
def blog(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    if blog:
        return render_template('blog.html', blog=blog)
    else:
        # flash('Blog not found.', 'error')
        return redirect('/blogs')

@app.route('/courses/<slug>')
def course_post(slug):
    course = Course.query.filter_by(slug=slug).first()
    current_date = date.today()
    if course:
        return render_template('course.html', course=course, current_date=current_date)
    else:
        # flash('Course not found.', 'error')
        return redirect('/courses')
    

@app.route('/admin-dashboard/add-quiz')
def add_quiz():
    if 'admin' in session:
        courses = Course.query.all()
        return render_template('add_quiz.html', courses=courses)
    else:
        return redirect('/admin-login')



@app.route('/admin-dashboard/create-quiz/<int:course_id>')
def create_quiz(course_id):
    if 'admin' in session:
        course = Course.query.get(course_id)
        return render_template('create_quiz.html', course=course)
    else:
        return redirect('/admin-login')

@app.route('/admin-dashboard/save-quiz/<int:course_id>', methods=['POST'])
def save_quiz(course_id):
    if 'admin' in session:
        course = Course.query.get(course_id)
        
        quiz = Quiz(course_id=course_id)
        for i in range(20):
            question_content = request.form.get(f'question_{i+1}')
            question = Question(content=question_content, quiz=quiz)
            
            for j in range(4):
                option_content = request.form.get(f'option_{i+1}_{j+1}')
                is_correct = (j == 0)  # Set the first option as correct
                
                option = Option(content=option_content, is_correct=is_correct, question=question)
                db.session.add(option)
            db.session.add(question)
        
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz added successfully.', 'success')
        return redirect('/admin-dashboard')
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/edit-quizzes')
def edit_quizzes():
    if 'admin' in session:
        quizzes = Quiz.query.all()
        return render_template('edit_quizzes.html', quizzes=quizzes)
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    if 'admin' in session:
        quiz = Quiz.query.get(quiz_id)

        if request.method == 'POST':
            # Update the quiz details
            quiz.course_id = request.form.get('course_id', quiz.course_id)

            # Retrieve the existing questions and options
            existing_questions = quiz.questions
            existing_options = Option.query.filter(Option.question_id.in_([question.id for question in existing_questions]))

            # Update the existing questions and options
            for question in existing_questions:
                question_content = request.form.get(f'question_{question.id}')
                if question_content is not None:
                    question.content = question_content

            for option in existing_options:
                option_content = request.form.get(f'option_{option.question_id}_{option.id}')
                is_correct = request.form.get(f'correct_option_{option.question_id}')
                if option_content is not None and is_correct is not None:
                    option.content = option_content
                    option.is_correct = (option.id == int(is_correct))

            # Add new questions and options
            for i in range(1, 21):
                new_question_content = request.form.get(f'new_question_{i}')
                if new_question_content:
                    new_question = Question(content=new_question_content, quiz=quiz)

                    for j in range(1, 5):
                        new_option_content = request.form.get(f'new_option_{i}_{j}')
                        new_correct_option = request.form.get(f'new_correct_option_{i}')
                        if new_option_content:
                            is_correct = (j == int(new_correct_option)) if new_correct_option else False
                            new_option = Option(content=new_option_content, is_correct=is_correct, question=new_question)
                            db.session.add(new_option)

                    db.session.add(new_question)

            db.session.commit()

            flash('Quiz updated successfully!', 'success')
            return redirect('/admin-dashboard/edit-quizzes')

        return render_template('edit_quiz.html', quiz=quiz)
    else:
        return redirect('/admin-login')


@app.route('/admin-dashboard/delete-quiz/<int:quiz_id>', methods=['GET'])
def delete_quiz(quiz_id):
    if 'admin' in session:
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            flash('Quiz deleted successfully!', 'success')
            return redirect('/admin-dashboard/edit-quizzes')
        else:
            flash('Quiz not found.', 'error')

        return redirect('/admin-dashboard/edit-quizzes')
    else:
        return redirect('/admin-login')







@app.route('/admin/view-applications')
def view_applications():
    if 'admin' in session:
        courses = Course.query.all()
        return render_template('view_applications.html', courses=courses)
    else:
        return redirect('/admin-login')


@app.route('/admin/view-applications/<int:course_id>')
def view_course_applications(course_id):
    if 'admin' in session:
        course = Course.query.get(course_id)
        if course:
            applications = course.applications
            return render_template('view_course_applications.html', course=course, applications=applications)
        else:
            flash('Course not found.', 'error')
            return redirect('/admin/view-applications')
    else:
        return redirect('/admin-login')


@app.route('/admin/accept-application/<int:application_id>', methods=['POST'])
def accept_application(application_id):
    if 'admin' in session:
        application = Application.query.get(application_id)
        if application:
            # Update the application status to "Paid"
            application.status = 'Paid'
            db.session.commit()
            
            # Send an email to the user
            send_acceptance_email(application.user)

            flash('Application accepted successfully!', 'success')
            return redirect(url_for('view_course_applications', course_id=application.course_id))
        else:
            flash('Application not found.', 'error')
            return redirect(url_for('view_applications'))
    else:
        return redirect('/admin-login')


def send_acceptance_email(user):
    msg = Message('Application Accepted', sender=recipient, recipients=[user.email])
    msg.html = render_template('acceptance_email.html', user=user)
    mail.send(msg)




@app.route('/admin/delete-application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    if 'admin' in session:
        application = Application.query.get(application_id)
        if application:
            # Update the application status to "Cancelled"
            application.status = 'Cancelled'
            db.session.commit()
            flash('Application deleted successfully!', 'success')

            # Get the course ID before redirecting
            course_id = application.course_id

            # Retrieve the updated list of applications
            course = Course.query.get(course_id)
            applications = course.applications

            return redirect(url_for('view_course_applications', course_id=course_id, applications=applications))
        else:
            flash('Application not found.', 'error')
            return redirect(url_for('view_applications'))
    else:
        return redirect('/admin-login')


@app.route('/application_success')
def application_success():
    return render_template('application_success.html')


@app.route('/apply-now/<int:course_id>', methods=['GET', 'POST'])
@login_required
def apply_now(course_id):
    # Retrieve the course details based on the course_id
    course = Course.query.get(course_id)
    user = current_user

    if user in course.registered_users:
        flash('You have already registered for this course.', 'warning')
        return redirect(url_for('dashboard'))


    if request.method == 'POST':
        # Check if the user has already applied for this course
        existing_application = Application.query.filter_by(user_id=user.id, course_id=course.id).first()
        if existing_application:
            flash('You have already submitted an application for this course.', 'warning')
            return redirect(url_for('dashboard'))

        return redirect(url_for('application_form', course_id=course_id))

    return render_template('apply_now.html', course=course, user=user)


@app.route('/application-form/<int:course_id>', methods=['GET', 'POST'])
@login_required
def application_form(course_id):
    # Retrieve the course details based on the course_id
    course = Course.query.get(course_id)
    user = current_user

    # Get a list of all countries
    countries = list(pycountry.countries)

    if request.method == 'POST':
        # Retrieve the application form data
        phone = request.form.get('phone')
        country_code = request.form.get('country')
        state = request.form.get('state')
        education = request.form.get('education')
        skills = request.form.get('skills')
        time = request.form.get('time')
        motivation = request.form.get('motivation')

        # Get the country name from the country code
        country = None
        for c in countries:
            if c.alpha_2 == country_code:
                country = c.name
                break

        # Create a new application object
        application = Application(
            user_id=user.id,
            course_id=course.id,
            phone=phone,
            country=country,
            state=state,
            education=education,
            skills=skills,
            time=int(time),
            motivation=motivation,
            status='Pending'
        )

        # Add the application to the database
        db.session.add(application)
        db.session.commit()

        # Redirect to the application success page
        return redirect(url_for('application_success'))

    return render_template('application_form.html', course=course, user=user, countries=countries)






# TODO 

# @app.route('/quiz/<int:course_id>', methods=['GET', 'POST'])
# def quiz(course_id):
#     # Retrieve the course details based on the course_id
#     course = Course.query.get(course_id)
#     quiz = course.quizzes[0]  # Assuming each course has only one quiz

#     # Retrieve the quiz questions for the course
#     questions = quiz.questions
#     num_questions = len(questions)

#     # Shuffle the options for each question
#     for question in questions:
#         random.shuffle(question.options)

#     # Get the current question index from the session or set it to 0
#     current_question_index = session.get('current_question_index', 0)

#     if request.method == 'POST':
#         # Handle form submission if needed
#         user_answers = {}

#         for question in questions:
#             user_answer = request.form.get(f'question_{question.id}')
#             user_answers[question.id] = user_answer

#         # Store the user's answers in the session
#         session['user_answers'] = user_answers

#         if 'submit' in request.form:
#             # Submit the quiz and calculate the score
#             score = 0

#             for question in questions:
#                 user_answer = user_answers[question.id]
#                 correct_option_id = question.options[0].id

#                 if user_answer == str(correct_option_id):
#                     score += 1

#             # Calculate the overall grade as a percentage
#             overall_grade = (score / num_questions) * 100

#             # Render the quiz result page with the user's score and overall grade
#             return render_template('quiz_result.html', score=score, overall_grade=overall_grade)

#         elif 'next' in request.form:
#             # Move to the next question
#             current_question_index += 1

#             if current_question_index == num_questions - 1:
#                 # On the last question, change the button text to "Submit"
#                 next_button_text = 'Submit'
#             else:
#                 next_button_text = 'Next'

#             # Update the current question index in the session
#             session['current_question_index'] = current_question_index

#             # Render the quiz page with the next question
#             return render_template('quiz.html', course=course, quiz=quiz, questions=questions,
#                                    num_questions=num_questions, current_question_index=current_question_index,
#                                    next_button_text=next_button_text)

#         elif 'prev' in request.form:
#             # Move to the previous question
#             if current_question_index > 0:
#                 current_question_index -= 1
#             else:
#                 current_question_index = 0

#             if current_question_index == num_questions - 1:
#                 # When going back from the last question, change the button text back to "Next"
#                 next_button_text = 'Next'
#             else:
#                 next_button_text = 'Submit' if current_question_index == num_questions - 1 else 'Next'

#             # Update the current question index in the session
#             session['current_question_index'] = current_question_index

#             # Render the quiz page with the previous question
#             return render_template('quiz.html', course=course, quiz=quiz, questions=questions,
#                                    num_questions=num_questions, current_question_index=current_question_index,
#                                    next_button_text=next_button_text)

#     else:
#         # Reset the session variables when starting a new quiz
#         session['current_question_index'] = 0
#         session['user_answers'] = {}

#     # Render the quiz page with the first question
#     return render_template('quiz.html', course=course, quiz=quiz, questions=questions,
#                            num_questions=num_questions, current_question_index=0, next_button_text='Next')


@app.route('/quiz-instructions/<int:course_id>', methods=['GET', 'POST'])
def quiz_instructions(course_id):
    if request.method == 'POST':
        return redirect(url_for('quiz', course_id=course_id))

    course = Course.query.get(course_id)
    return render_template('quiz_instructions.html', course=course)


# TODO



@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'success')
    return redirect('/admin-login')



#default error handler for invalid pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404




## ----- ROUTES ENDS ----- ##




