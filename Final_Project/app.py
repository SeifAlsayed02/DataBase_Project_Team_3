# from flask import Flask, render_template, request, redirect, session
# import psycopg2
# import psycopg2.extras
# from werkzeug.utils import secure_filename
# import os

# app = Flask(__name__)
# app.secret_key = 'xyz3231'
# app.config['UPLOAD_FOLDER'] = 'static/uploads/profile_images'
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# database_session = psycopg2.connect(
#     database='postgres',
#     port=5432,
#     host='localhost',
#     user='postgres',
#     password='12345678'
# )
# cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# @app.route('/home')
# def home_page():

#     return render_template('index.html')
# @app.route('/',methods=['GET','POST'])
# def home():
#     msg = ''
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email:
#         cursor.execute('SELECT id, username FROM patient where email = %s and password = %s',
#                        (email, password))
#         result = cursor.fetchone()
#         if result:
#             session['user'] = dict(
#                 result)
#             return redirect('/home')
#             # return render_template('index.html', user=dict(result))
#             pass
#         else:
#             msg = 'Please enter correct email/password'
#     return render_template('index.html', msg=msg)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     message = ''
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email:
#         cursor.execute('SELECT id, username FROM patient where email = %s and password = %s',
#                        (email, password))
#         result = cursor.fetchone()
#         if result:
#             session['user'] = dict(
#                 result)
#             return redirect('/home')
#             # return render_template('index.html', user=dict(result))
#             pass
#         else:
#             message = 'Please enter correct email/password'
#     return render_template('login.html' , msg=message)
# @app.route('/appointment')
# def appointment():
#     return render_template('appointment.html')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     message = ''
#     if request.method == 'POST':
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         midname = request.form.get('midname')
#         phone = request.form.get('phone')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         profile_image = None

#         cursor.execute('SELECT email FROM patient where email = %s', (email,))
#         if cursor.fetchone():
#             message = 'Account already exists!'
#         else:
#             if 'profile_image' in request.files:
#                 file = request.files['profile_image']
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                     file.save(filepath)
#                     profile_image = filename

#             try:
#                 cursor.execute('INSERT INTO patient(fname,midname,lname,email,phone,password,profile_image) VALUES (%s ,%s, %s, %s ,%s, %s, %s)',
#                                (fname,midname,lname,email, phone, password, profile_image))
#                 database_session.commit()
#                 message = 'You have successfully registered'
#                 return redirect('/login')
#             except psycopg2.DatabaseError as e:
#                 database_session.rollback()
#                 message = str(e)
#                 print("Database Error: ", e)

#     return render_template('register.html', msg=message)

# @app.route('/profilepage', methods=['GET', 'POST'])
# def profilepage():
#     # Check if user is logged in
#     if 'user' not in session or not session['user']:
#         return redirect('/index')

#     user_id = session['user']['id']
#     cursor.execute('SELECT  fname,midname, lname,email, phone, profile_image FROM patient WHERE id = %s', (user_id,))
#     patient = cursor.fetchone()

#     if patient is None:
#         return redirect('/index')
#     return render_template('profile.html', user=patient)

# @app.route('/editprofile', methods=['GET', 'POST'])
# def edit_profile():
#     if 'user' not in session or not session['user']:
#         return redirect('/login')

#     user_id = session['user']['id']
#     message = ''

#     if request.method == 'POST':
#         new_password = request.form.get('password')
#         new_phone = request.form.get('phone')
#         profile_image = None
#         if 'profile_image' in request.files:
#             file = request.files['profile_image']
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(filepath)
#                 profile_image = filename

#         update_fields = {}
#         if new_password:
#             update_fields['password'] = new_password
#         if new_phone:
#             update_fields['phone'] = new_phone
#         if profile_image:
#             update_fields['profile_image'] = profile_image

#         # Construct the update query based on the fields provided
#         if update_fields:
#             update_query = 'UPDATE patient SET '
#             update_query += ', '.join([f"{key} = %s" for key in update_fields.keys()])
#             update_query += ' WHERE id = %s'

#             cursor.execute(update_query, list(update_fields.values()) + [user_id])
#             database_session.commit()
#             message = 'Profile updated successfully.'
#         else:
#             message = 'No changes made to the profile.'
#     return render_template('editprofile.html', msg=message)


# @app.route('/Postpartum Check-ups appointment', methods=['GET', 'POST'])
# def postpartum_check_ups_doctors():
#     message = ''
#     if request.method == 'POST':
#         ssn = request.form['ssn']
#         fname = request.form.get('fname')
#         midname = request.form.get('midname')
#         age = request.form.get('age')
#         gender = request.form.get('gender')
#         doctor_name = request.form.get('doctor')
#         cursor.execute('INSERT INTO appointment(ssn,fname,midname,age,gender,doctor_name) VALUES (%s ,%s, %s, %s ,%s,%s)',
#             (ssn,fname, midname, age, gender,doctor_name))
#         database_session.commit()
#         message = 'You have successfully registered'
#         return redirect('/home')
#     cursor.execute("SELECT id, fname, lname FROM doctor WHERE specialization = 'postpartum'")
#     doctors = cursor.fetchall()
#     return render_template('Postpartum Check-ups doctors.html', msg=message,doctors=doctors)

# @app.route('/Parental appointment', methods=['GET', 'POST'])
# def parental_appointment():
#     message = ''
#     if request.method == 'POST':
#         ssn = request.form['ssn']
#         fname = request.form.get('fname')
#         midname = request.form.get('midname')
#         age = request.form.get('age')
#         gender = request.form.get('gender')
#         doctor_name = request.form.get('doctor')
#         cursor.execute('INSERT INTO appointment(ssn,fname,midname,age,gender,doctor_name) VALUES (%s ,%s, %s, %s ,%s,%s)',
#             (ssn,fname, midname, age, gender,doctor_name))
#         database_session.commit()
#         message = 'You have successfully registered'
#         return redirect('/home')
#     cursor.execute("SELECT id, fname, lname FROM doctor WHERE specialization = 'parental_care'")
#     doctors = cursor.fetchall()
#     return render_template('Prenatal Care Visits doctors.html', msg=message,doctors=doctors)
# @app.route('/annualexamination', methods=['GET', 'POST'])
# def annualexamination():
#     message = ''
#     if request.method == 'POST':
#         ssn = request.form['ssn']
#         fname = request.form.get('fname')
#         midname = request.form.get('midname')
#         age = request.form.get('age')
#         gender = request.form.get('gender')
#         doctor_name = request.form.get('doctor')
#         cursor.execute('INSERT INTO appointment(ssn,fname,midname,age,gender,doctor_name,service) VALUES (%s ,%s, %s, %s ,%s,%s,%s)',
#             (ssn,fname, midname, age, gender,doctor_name,"annualexamination"))
#         database_session.commit()
#         message = 'You have successfully registered'
#         return redirect('/home')
#     cursor.execute("SELECT id, fname, lname FROM doctor WHERE specialization = 'annual_examinations'")
#     doctors = cursor.fetchall()
#     return render_template('Annual Well-Woman Exams doctors.html', msg=message,doctors=doctors)


# @app.route('/adminlogin' , methods=['GET', 'POST'])
# def admin_login():
#     message = ''
#     username = request.form.get('username')
#     password = request.form.get('password')
#     if username:
#         cursor.execute('SELECT id, username FROM admins where username = %s and password = %s',
#                        (username, password))
#         result = cursor.fetchone()
#         if result:
#             session['user'] = dict(
#                 result)
#             return redirect('/adminHome')
#             # return render_template('index.html', user=dict(result))
#             pass
#         else:
#             message = 'Please enter correct email/password'
#     return render_template('/admin/Admin.html', msg=message)


# @app.route('/adminHome')
# def admin_home():
#     return render_template('/admin/adminhome.html')


# @app.route('/doctors',methods=['GET', 'POST'])
# def admin_doctors():
#     message = ''
#     if request.method == 'POST':
#         # Assuming you have form fields with these names
#         fname = request.form['fname']
#         midname = request.form['midname']
#         lname = request.form['lname']
#         email = request.form['email']
#         age = request.form['age']
#         gender = request.form['gender']
#         phone = request.form['phone']
#         degree = request.form['degree']
#         ssn = request.form['ssn']
#         image = None
#         cursor.execute('SELECT * FROM doctor WHERE ssn = %s OR phone = %s OR email = %s', (ssn, phone, email))
#         existing_doctor = cursor.fetchone()
#         if existing_doctor:
#             message = 'A doctor with the provided SSN, phone number, or email already exists.', 'error'
#         else:
#             if 'image' in request.files:
#                 file = request.files['image']
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                     file.save(filepath)
#                     image = filename
#         try:
#             cursor.execute('INSERT INTO doctor (fname,midname,lname,email,age,gender,phone,degree,ssn, image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
#                         (fname, midname, lname, email, age, gender, phone, degree, ssn, image))
#             database_session.commit()
#             message = 'You have successfully registered'
#             return redirect('/doctors')
#         except psycopg2.DatabaseError as e:
#           database_session.rollback()
#           message = str(e)
#           print("Database Error: ", e)
#     cursor.execute('SELECT * FROM doctor')
#     doctor = cursor.fetchall()  # Fetch all doctors from the database
#     return render_template('admin/admin_doctors.html', doctor=doctor)


# @app.route('/adminappointment')
# def adminappointment():
#     cursor.execute('SELECT * FROM appointment')
#     appointment = cursor.fetchall()  # Fetch all doctors from the database
#     return render_template('/admin/adminapp.html',appointment=appointment)
# @app.route('/adminusers')
# def adminusers():

#     cursor.execute('SELECT * FROM patient')
#     patient = cursor.fetchall()  # Fetch all doctors from the database
#     return render_template('/admin/adminusers.html', patient=patient)


# @app.route('/logout')
# def logout():
#     session['user'] = None
#     return redirect('/',)

# if __name__ == '__main__':
#     app.run()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/postgres'
db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admins'
    code = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['POST'])
def login():
    The_email = request.form.get('exampleInputEmail1')
    The_password = request.form.get('exampleInputPassword1')

    # Search in Admin table
    admin = Admin.query.filter_by(email=The_email, password=The_password).first()
    if admin:
        return redirect(url_for('admin_dashboard', user_code=admin.code))

    # Search in Doctor table
    doctor = Doctor.query.filter_by(email=The_email, password=The_password).first()
    if doctor:
        return redirect(url_for('doctor_dashboard', user_id=doctor.id))

    # Search in Patient table
    patient = Patient.query.filter_by(email=The_email, password=The_password).first()
    if patient:
        return redirect(url_for('patient_dashboard', user_id=patient.id))

    # If no user is found
    return render_template('index.html', error='Invalid login credentials')

    
@app.route('/signup/patient', methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        username = request.form.get('username')  # Add this line
        email = request.form.get('email')
        password = request.form.get('password')

        # Create a new Patient instance
        new_patient = Patient(name=name, age=age, gender=gender, username=username, email=email, password=password)

        # Add the new patient to the database
        db.session.add(new_patient)
        db.session.commit()

        # Redirect to the patient dashboard with the new user's ID
        return redirect(url_for('patient_dashboard', user_id=new_patient.id))

    return render_template('signup_patient.html')

@app.route('/signup/doctor', methods=['GET', 'POST'])
def signup_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        username = request.form.get('username') 
        email = request.form.get('email')
        password = request.form.get('password')

        # Create a new doctor instance
        new_doctor = Doctor(name=name, age=age, gender=gender, username=username, email=email, password=password)

        # Add the new doctor to the database
        db.session.add(new_doctor)
        db.session.commit()

        # Redirect to the doctor dashboard with the new user's ID
        return redirect(url_for('doctor_dashboard', user_id=new_doctor.id))

    return render_template('signup_doctor.html')

@app.route('/admin/dashboard/<string:user_code>')
def admin_dashboard(user_code):
    user = Admin.query.get(user_code)
    if user:
        print(user.code)
        print(user.username)
        print(user.email)
    return render_template('patient_dashboard.html')

@app.route('/doctor/dashboard/<int:user_id>')
def doctor_dashboard(user_id):
    user = Doctor.query.get(user_id)
    if user:
        print(user.id)
        print(user.username)
        print(user.email)
    return render_template('patient_dashboard.html')

@app.route('/patient/dashboard/<int:user_id>')
def patient_dashboard(user_id):
    user = Patient.query.get(user_id)
    if user:
        print(user.id)
        print(user.username)
        print(user.email)
        print("Reached the /patient/dashboard route!")
    return render_template('patient_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
