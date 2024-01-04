
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'haha'
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


class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointmentid = db.Column(db.Integer, primary_key=True)
    appointmentdate = db.Column(db.Date, nullable=False)
    appointmenttime = db.Column(db.Time, nullable=False)
    doctorid = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patientid = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)


class Scan(db.Model):
    __tablename__ = 'scans'
    scanid = db.Column(db.Integer, primary_key=True)
    scandate = db.Column(db.Date, nullable=False)
    scantime = db.Column(db.Time, nullable=False)
    doctorid = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patientid = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

class ScanFile(db.Model):
    __tablename__ = 'scanfiles'
    scanid = db.Column(db.Integer, primary_key=True)
    #scanid = db.Column(db.Integer, db.ForeignKey('scans.scan_id'), nullable=False)
    file = db.Column(db.Text, nullable=False)

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    prescriptionid = db.Column(db.Integer, primary_key=True)
    prescriptiondate = db.Column(db.Date, nullable=False)
    prescriptiontime = db.Column(db.Time, nullable=False)
    doctorid = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patientid = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

class PrescriptionFile(db.Model):
    __tablename__ = 'prescriptionfiles'
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=False)
    file = db.Column(db.Text, nullable=False)

@app.route('/patient/dashboard/<int:user_id>', methods=['GET', 'POST'])
def patient_dashboard(user_id):
    user = Patient.query.get(user_id)
    doctors = Doctor.query.all()
    scanfiles = ScanFile.query.all()

    # Fetch patient's appointments
    appointments = Appointment.query.filter_by(patientid=user_id).all()
    scans = Scan.query.filter_by(patientid=user_id).all()
    prescriptions = Prescription.query.filter_by(patientid=user_id).all()

    if request.method == 'POST':
        print("Form submitted")
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        doctor_id = request.form.get('doctor_id')
        message = request.form.get('message')
        print(f"Date: {appointment_date}, Time: {appointment_time}, Doctor ID: {doctor_id}, Message: {message}")
        new_appointment = Appointment(
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            doctor_id=doctor_id,
            patient_id=user_id,
            message=message
        )

        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('patient_dashboard', user_id=user_id))

    return render_template('patient_dashboard.html', user=user, doctors=doctors,scanfiles=scanfiles, appointments=appointments, scans=scans, prescriptions=prescriptions)


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



if __name__ == '__main__':
    app.run(debug=True)
