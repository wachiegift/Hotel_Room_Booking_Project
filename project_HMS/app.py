
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
from flask import Flask, render_template,url_for,request,redirect,session
#from requests import session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hi'
# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rakesh@9999",
    database="hms"
)

# HOME PAGE 

@app.route('/ex_navbar' , methods = ['GET', 'POST'])
def homePage1():
    if request.method == 'POST':
        username = request.form['Uname']
        email = request.form['mail']
        Phone_Number=request.form['no']
        age = request.form['age']
        Password=request.form['Pass']
        city=request.form['cliv']
        # Perform registration logic by inserting data into the database
        cursor = db.cursor()
        query = "INSERT INTO logindb (uname,email,phone,age,password,city) VALUES (%s, %s, %s,%s, %s, %s)"
        cursor.execute(query, (username,email,Phone_Number,age,Password,city))
        db.commit()
        return render_template('ex_navbar.html')

def bill():
    single_cost = 2000
    double_cost = 3500
    suite_cost = 4500
        
    # Assuming you have a cursor object
    cursor = db.cursor()
    username = session.get('USERNAME')
    password = session.get('PASSWORD')
    # SQL query to retrieve check-in, check-out, and room details
    query = "SELECT checkin, checkout, singleroom, doubleroom, suitroom FROM roombookdb WHERE username = %s AND password = %s"

    # Execute the query
    cursor.execute(query,(username, password))

    # Fetch the results
    result = cursor.fetchone()

    # Check if there is a result
    if result:
        # Store the values in individual variables
        cin = result[0]
        cout = result[1]
        single_rooms = int(result[2])
        double_rooms = int(result[3])
        suite_rooms = int(result[4])
    else:
        print("No data found for the given username and password")


    # Get the check-in and check-out dates from the form or database
    check_in_date = datetime.strptime(cin.strftime('%Y-%m-%d'), '%Y-%m-%d')
    check_out_date = datetime.strptime(cout.strftime('%Y-%m-%d'), '%Y-%m-%d')

    # Calculate the number of days stayed
    duration = check_out_date - check_in_date
    num_days = duration.days

    # Calculate the room charges
    single_room_charges = single_rooms * single_cost * num_days
    double_room_charges = double_rooms * double_cost * num_days
    suite_room_charges = suite_rooms * suite_cost * num_days

    # Calculate the total cost
    total_cost = single_room_charges + double_room_charges + suite_room_charges

    room_details = []

    # Append room details to the list if count is greater than zero
    if single_rooms > 0:
        room_details.append(f"Number of Single Rooms: {single_rooms}")
    if double_rooms > 0:
        room_details.append(f"Number of Double Rooms: {double_rooms}")
    if suite_rooms > 0:
        room_details.append(f"Number of Suite Rooms: {suite_rooms}")

    # Construct the email body with conditionally displayed room details
    body = """
    <html>
    <head></head>
    <body>
    <h2>Hotel Bill</h2>
    <p>Check-in Date: {cin}</p>
    <p>Check-out Date: {cout}</p>
    {room_details}
    <p>Total Cost: {total}</p>
    </body>
    </html>
    """.format(cin=cin, cout=cout, room_details="<br>".join(room_details), total=total_cost)

    return body

@app.route('/ex_navbarbook' , methods = ['GET', 'POST'])
def homePage2():
    if request.method == 'POST':
        single = request.form['single']
        double = request.form['double']
        suit=request.form['suit']
        username = session.get('USERNAME')
        password = session.get('PASSWORD')
        # Perform registration logic by inserting dausername, passwordta into the database
        cursor = db.cursor()
        query = "UPDATE roombookdb SET singleroom = %s, doubleroom = %s, suitroom = %s WHERE username = %s AND password = %s"
        cursor.execute(query, (single, double, suit,username,password ))
        db.commit()

    
        # SQL query to retrieve check-in, check-out, and room details
        query = "SELECT email FROM logindb WHERE uname = %s AND password = %s"

        # Execute the query
        cursor.execute(query,(username, password))

        # Fetch the results
        result = cursor.fetchone()

        # Check if there is a result
        if result:
            # Store the values in individual variables
            email = result[0]
        else:
            print("No data found for the given username and password")
        
        subject = 'Your Hotel Bill'
        body=bill()
        message = f'{body}'

        if send_email(email, subject, message):
            return render_template('ex_navbar.html')
        else:
            return 'Failed to send OTP'

        
@app.route('/')
def homePage():
    return render_template('ex_navbar.html')

@app.route('/services/room')
def room_services():
    return render_template('ex_room_services.html')

@app.route('/services/food')
def food_services():
    return render_template('ex_food_services.html')

@app.route('/services/other')
def other_services():
    return render_template('other_services.html')


# LOGIN

@app.route('/login' , methods = ['POST', 'GET'])
def login_pro():
        return render_template('ex_login_page.html')


@app.route('/Users',methods = ['POST', 'GET'])
def Users():
   if request.method == 'POST':
      return render_template("after_login.html")


app.secret_key = 'hello'


def generate_otp():
    # Generate a 6-digit random OTP
    return str(random.randint(100000, 999999))

def send_email(to_address, subject, message):
    try:
        # Configure your SMTP settings
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = 587
        SMTP_USERNAME = 'rakeshnakka2222@gmail.com'  # Replace with your Gmail address
        SMTP_PASSWORD = "wphoscmspngtgrkm"           #'niuftiskmnapgdcw'
        
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_address
        msg['Subject'] = subject

        # Attach the HTML message
        msg.attach(MIMEText(message, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        return False
        
    """
        # Connect to the SMTP server
        
        server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Create the email message
        email_message = f'Subject: {subject}\n\n{message}'
        
        # Send the email
        server.sendmail(SMTP_USERNAME, to_address, email_message)
        server.quit()

        return True
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        return False"""

# REGISTRATION 
@app.route('/Registration', methods=['GET', 'POST'])
def Registration():
    return render_template('ex_registration_page1.html')

@app.route('/RegistrationData', methods=['GET', 'POST'])
def RegistrationData():
    if request.method == 'POST':
            email = request.form['mail']
            otp = generate_otp()
            session['OTP'] = otp
            # Send the OTP via email
            subject = 'OTP Verification'
            message = f'Your OTP is: {otp}'
            if send_email(email, subject, message):
                return render_template('ex_registration_page1-otp.html')
            else:
                return 'Failed to send OTP'
@app.route('/Registration2')
def Registration2():
    return render_template('ex_registration_page2.html')

@app.route('/RegistrationOTP', methods=['GET', 'POST'])
def RegistrationOTP():
    
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        stored_otp =session.get('OTP')  

        if entered_otp == stored_otp:
            return render_template('ex_registration_page2.html')
        else:
            return 'Invalid OTP'
    #return render_template('ex_registration_page1-otp.html')

#AFTER --- LOGIN 

@app.route('/after_login' , methods = ['POST', 'GET'])
def after_login():
        return render_template('after_login.html')

@app.route('/Bookroompage1')
def Bookroompage1():
    return render_template('ex_bookroom_page1.html')

@app.route('/Bookroompage2', methods = ['POST', 'GET'])
def Bookroompage2():
     if request.method == 'POST':
        cin = request.form['cin']
        cout = request.form['cout']

        username = session.get('USERNAME')
        password = session.get('PASSWORD')

        # Perform registration logic by inserting data into the database
        cursor = db.cursor()
        query = "INSERT INTO roombookdb (username,password,checkin,checkout) VALUES (%s, %s,%s, %s)"
        cursor.execute(query, (username,password,cin,cout))
        db.commit()
        return render_template('ex_bookroom_page2.html')



@app.route('/login',methods = ['POST', 'GET'])
def login():
    return render_template('ex_login_page.html')
 

@app.route('/profile',methods = ['POST', 'GET'])
def profile():
     if request.method == 'POST':
        username = request.form['Uname']
        password = request.form['Pass']
        
        session['USERNAME'] = username
        session['PASSWORD'] = password
        # Perform authentication logic by querying the database
        cursor = db.cursor()
        query = "SELECT * FROM logindb WHERE uname = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            # Store username in session
            #session['username'] = username
            # Redirect to the home page on successful login
            #return redirect(url_for('profile', username=username))
            return render_template('after_login.html', username=username)
        else:
            # Display an error message if login is unsuccessful
            error_message = 'Invalid username or password.'
            return render_template('sample.html', error_message=error_message)
     #return render_template('after_login.html', username=username)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)