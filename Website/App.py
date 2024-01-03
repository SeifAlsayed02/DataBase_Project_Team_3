from flask import Flask, render_template, request, redirect, session
import psycopg2
import psycopg2.extras
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = 'xyz3231'
app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/postgres'
# app.config['UPLOAD_FOLDER'] = 'static/uploads/profile_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
database_session = psycopg2.connect(
    database='postgres',
    port=5432,
    host='localhost',
    user='postgres',
    password='1234567890'
)
cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# @app.route('/signup_admin')
# def home_page():
#     return render_template('signup_admin.html')
# @app.route('/',methods=['GET','POST'])
# def home():
#     msg = ''
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if email:
#         cursor.execute('SELECT id, username FROM patient where email = %s and password = %s',(email, password))
#         result = cursor.fetchone()
#         if result:
#             session['user'] = dict(result)
#             return redirect('/home')
#             # return render_template('index.html', user=dict(result))
#             pass
#         else:
#             msg = 'Please enter correct email/password'
#     return render_template('signup_admin.html', msg=msg)

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

@app.route('/signup_doctor', methods=['GET', 'POST'])
def signup_doctor():
    message = ''
    if request.method == 'POST':
        name = request.form.get('name') 
        username = request.form.get('username') #lesa
        phone = request.form.get('phone') 
        email = request.form.get('email')
        password = request.form.get('password')
        Repeatedpassword = request.form.get('Repeatedpassword')
        dateOfBirth = request.form.get('age') #how to convert date of birth to age?
        ##
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        midname = request.form.get('midname')
        # profile_image = None ## lesa
        ##
        cursor.execute('SELECT email FROM doctors where email = %s', (email,))
        if cursor.fetchone():
            message = 'Account already exists!'
        else:
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                # if file and allowed_file(file.filename):
                #     filename = secure_filename(file.filename)
                #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                #     file.save(filepath)
                #     profile_image = filename
            try:
                cursor.execute('INSERT INTO doctors(name,username,phone,email,password,Repeatedpassword,age,profile_image) VALUES (%s ,%s, %s, %s, %s ,%s, %s)',
                               (name,username, phone, email, password,Repeatedpassword, dateOfBirth))
                database_session.commit()
                message = 'You have successfully registered'
                return redirect('/index')
            except psycopg2.DatabaseError as e:
                database_session.rollback()
                message = str(e)
                print("Database Error: ", e)

    return render_template('signup_doctor.html', msg=message)

if __name__ == '__main__':
    app.run()