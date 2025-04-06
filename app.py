from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database import init_db, add_booking, get_room_types, check_availability, delete_booking
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Existing routes remain unchanged until admin_dashboard
@app.route('/')
def index():
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/room_types')
def room_types():
    rooms = get_room_types()
    return render_template('room_types.html', rooms=rooms)

@app.route('/room_booking', methods=['GET', 'POST'])
def room_booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        room_type = request.form['room_type']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        
        if check_availability(room_type, check_in, check_out):
            add_booking(name, email, room_type, check_in, check_out)
            return redirect(url_for('index'))
        else:
            return "Room not available for selected dates!"
    return render_template('room_booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return "Invalid credentials!"
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', bookings=bookings)

# New route to remove a booking
@app.route('/admin/remove/<int:booking_id>', methods=['POST'])
def remove_booking(booking_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    delete_booking(booking_id)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)