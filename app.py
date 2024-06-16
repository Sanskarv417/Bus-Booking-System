from flask import Flask, session, render_template, request, redirect, flash, g
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sanskar@417'
app.config['MYSQL_DATABASE_DB'] = 'bus-booking-system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin[2], password):
            session['admin_id'] = admin[0]
            return redirect('/admin/dashboard')
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin_login.html')

# Admin register route
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        hashed_password = generate_password_hash(password, method='sha256')

        cursor = mysql.get_db().cursor()
        cursor.execute('INSERT INTO admin (username, password, email) VALUES (%s, %s, %s)',
                       (username, hashed_password, email))
        mysql.get_db().commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect('/admin/login')

    return render_template('admin_register.html')

# Admin reset password route
@app.route('/admin/reset-password', methods=['GET', 'POST'])
def admin_reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        hashed_password = generate_password_hash(new_password, method='sha256')

        cursor = mysql.get_db().cursor()
        cursor.execute('UPDATE admins SET password = %s WHERE username = %s',
                       (hashed_password, username))
        mysql.get_db().commit()

        flash('Password reset successful. Please login with your new password.', 'success')
        return redirect('/admin/login')

    return render_template('admin_reset_password.html')

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        cursor.execute('SELECT * FROM user')
        user = cursor.fetchall()
        return render_template('admin_dashboard.html',user=user)
    else:
        return redirect('/admin/login')
    
# Route to view all users
@app.route('/admin/view_users')
def view_users():
    cursor.execute('SELECT * FROM user')
    user = cursor.fetchall()
    return render_template('admin_viewing_users.html', users=user)    
    
# Route for managing buses
@app.route('/admin/manage_buses')
def manage_buses():
    if 'admin_id' in session:
        cursor.execute('SELECT * FROM bus')
        buses = cursor.fetchall()
        return render_template('admin_manage_buses.html', buses=buses)
    else:
        return render_template('admin_login.html')
    
# Route for adding a bus
@app.route('/admin/add_bus', methods=['GET', 'POST'])
def add_bus():
    if 'admin_id' in session:
        if request.method == 'POST':
            bus_name = request.form['bus_name']
            total_seats = request.form['total_seats']
            current_occupancy = request.form['current_occupancy']
            available_days = ",".join(request.form.getlist('available_days'))
            source_city = request.form['source_city']
            destination_city = request.form['destination_city']
            route_time = request.form['route_time']
            route_distance = request.form['route_distance']
            cursor.execute('INSERT INTO bus (bus_name, total_seats, current_occupancy, available_days, source_city, destination_city, route_time, route_distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                           (bus_name, total_seats, current_occupancy, available_days, source_city, destination_city, route_time, route_distance))
            
            bus_id = cursor.lastrowid 
            seats_data = [(bus_id, seat_number + 1, False) for seat_number in range(int(total_seats))]
            cursor.executemany('INSERT INTO seats (bus_id, seat_number, is_booked) VALUES (%s, %s, %s)', seats_data)
            
            conn.commit()
            cursor.execute('SELECT * FROM bus')
            buses = cursor.fetchall()
            return render_template('admin_manage_buses.html',buses=buses)
        return render_template('admin_add_bus.html')
    else:
        return render_template('admin_login.html')
    
# Route for updating a bus
@app.route('/admin/update_bus/<int:bus_id>', methods=['GET', 'POST'])
def update_bus(bus_id):
    if 'admin_id' in session:
        if request.method == 'POST':
            bus_name = request.form['bus_name']
            total_seats = request.form['total_seats']
            current_occupancy = request.form['current_occupancy']
            available_days = ",".join(request.form.getlist('available_days'))
            source_city = request.form['source_city']
            destination_city = request.form['destination_city']
            route_time = request.form['route_time']
            route_distance = request.form['route_distance']

            cursor.execute('UPDATE bus SET bus_name=%s, total_seats=%s, current_occupancy=%s, available_days=%s, source_city=%s, destination_city=%s, route_time=%s,route_distance=%s WHERE id=%s', (bus_name, total_seats, current_occupancy, available_days, source_city, destination_city, route_time, route_distance, bus_id)) 
            conn.commit()
            
            cursor.execute('SELECT * FROM bus')
            buses = cursor.fetchall()

            return render_template('admin_manage_buses.html',buses=buses)

        cursor.execute('SELECT * FROM bus WHERE id = %s', (bus_id,))
        bus = cursor.fetchone()

        return render_template('admin_update_bus.html', bus=bus)
    else:
        render_template('admin_login.html')
    
# Route for deleting a bus
@app.route('/admin/delete_bus/<int:bus_id>')
def delete_bus(bus_id):
    if 'admin_id' in session:
        cursor.execute('DELETE FROM bus WHERE id = %s', (bus_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM bus')
        buses = cursor.fetchall()
        
        return render_template('admin_manage_buses.html',buses=buses)
    else:
        return render_template('admin_login.html')


@app.route('/user/admin_manage_bookings')
def admin_manage_bookings():
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    return render_template('admin_manage_bookings.html', bookings=bookings)

# 
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect('/user/dashboard')
        else:
            flash('Invalid username or password', 'error')

    return render_template('user_login.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        cursor.execute('INSERT INTO user (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
        conn.commit()
        
        return render_template('user_login.html')
    
    return render_template('user_register.html')

# Route for user dashboard displaying available buses
@app.route('/user/dashboard')
def user_dashboard():
    if 'admin_id' in session:
        cursor.execute('SELECT * FROM bus')
        buses = cursor.fetchall()
        return render_template('user_dashboard.html', buses=buses)
    else:
        return redirect('/user/user_login')

# Route for checking seat availability
@app.route('/user/check_seat_availability/<int:bus_id>')
def check_seat_availability(bus_id):
    cursor.execute("SELECT * FROM bus WHERE id = %s", (bus_id,))
    bus = cursor.fetchone()
    if bus:
        cursor.execute("SELECT * FROM seats WHERE bus_id = %s", (bus_id,))
        seats = cursor.fetchone()
        return render_template('user_seat_availability.html', bus=bus,seats=seats)
    flash('Bus not found!', 'danger')
    return redirect('/user/user_dashboard')


@app.route('/user/manage_bookings/', methods=['GET', 'POST'])
def manage_bookings():
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')

        if booking_id:
            # Fetch booking details including bus_id and seat_number
            cursor.execute("SELECT bus_id, seat_number FROM bookings WHERE id = %s", (booking_id,))
            bookings = cursor.fetchone()

            bus_id = bookings[0]
            seat_number = bookings[1]
            
            if bookings:
                
                 # Start a transaction
                cursor.execute("START TRANSACTION")

                # Update seat status to booked
                cursor.execute("UPDATE seats SET is_booked = TRUE WHERE bus_id = %s AND seat_number = %s", (bus_id, seat_number))

                # Update other variables in bus table if needed (example: current_occupancy)
                cursor.execute("UPDATE bus SET current_occupancy = current_occupancy - 1 WHERE id = %s", (bus_id,))

                # Delete booking record from bookings table
                cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                conn.commit()

                flash('Booking successful!', 'success')
            else:
                flash('Booking not found!', 'danger')

            # Redirect back to manage bookings page after cancellation or error
            return render_template('user_manage_bookings.html')

    # Fetch all bookings for display
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    booking_id = request.form.get('booking_id')
    # return redirect(f'/manage_bookings/{booking_id}')
    return render_template('user_manage_bookings.html',bookings=bookings)

@app.route('/book_bus/<int:bus_id>', methods=['GET', 'POST'])
def book_bus(bus_id):
    if request.method == 'POST':
        seat_number = request.form.get('seat_number')

        # Check if the seat is available
        cursor.execute("SELECT * FROM seats WHERE bus_id = %s AND seat_number = %s AND is_booked = FALSE", (bus_id, seat_number))
        seat = cursor.fetchone()

        if seat:
            # Start a transaction
            cursor.execute("START TRANSACTION")

            # Update seat status to booked
            cursor.execute("UPDATE seats SET is_booked = TRUE WHERE bus_id = %s AND seat_number = %s", (bus_id, seat_number))

            # Insert booking record
            user_id = 1  # Replace with actual user ID
            cursor.execute("INSERT INTO bookings (user_id, bus_id, seat_number) VALUES (%s, %s, %s)", (user_id, bus_id, seat_number))

            # Update bus table - increase current occupancy
            cursor.execute("UPDATE bus SET current_occupancy = current_occupancy + 1 WHERE id = %s", (bus_id,))

            # Commit the transaction
            conn.commit()

            flash('Booking successful!', 'success')
            return redirect(f'/book_bus/{bus_id}')
        else:
            flash('Seat is not available for booking.', 'danger')

    # If GET request or after processing POST
    cursor.execute("SELECT * FROM bus WHERE id = %s", (bus_id,))
    bus = cursor.fetchone()

    if bus:
        # Fetch booked seats for the bus
        cursor.execute("SELECT seat_number FROM seats WHERE bus_id = %s AND is_booked = TRUE", (bus_id,))
        booked_seats = [seat[0] for seat in cursor.fetchall()]

        return render_template('user_book_bus.html', bus=bus, booked_seats=booked_seats)

    else:
        flash('Bus not found!', 'danger')
        return render_template('user_dashboard.html')


if __name__ == '__main__':
    app.secret_key = 'supersecretkey'  # Change this to a secure random key in production
    app.run(debug=True)
