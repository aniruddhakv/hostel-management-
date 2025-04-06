import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

def init_db():
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS room_types 
                 (id INTEGER PRIMARY KEY, type TEXT, price REAL, description TEXT, image TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, room_type TEXT, check_in TEXT, check_out TEXT)''')
    
    c.execute("INSERT OR IGNORE INTO room_types (id, type, price, description, image) VALUES (1, 'Single', 50.0, 'Cozy single room', 'single.jpg')")
    c.execute("INSERT OR IGNORE INTO room_types (id, type, price, description, image) VALUES (2, 'Double', 80.0, 'Spacious double room', 'double.jpg')")
    c.execute("INSERT OR IGNORE INTO room_types (id, type, price, description, image) VALUES (3, 'Dormitory', 30.0, 'Shared dorm with 6 beds', 'dorm.jpg')")
    conn.commit()
    conn.close()

def add_booking(name, email, room_type, check_in, check_out):
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, email, room_type, check_in, check_out) VALUES (?, ?, ?, ?, ?)",
              (name, email, room_type, check_in, check_out))
    conn.commit()
    conn.close()

def get_room_types():
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute("SELECT * FROM room_types")
    rooms = c.fetchall()
    conn.close()
    return rooms

def check_availability(room_type, check_in, check_out):
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM bookings WHERE room_type = ? AND ((check_in <= ?) AND (check_out >= ?))",
              (room_type, check_out, check_in))
    count = c.fetchone()[0]
    conn.close()
    return count == 0

def delete_booking(booking_id):
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()