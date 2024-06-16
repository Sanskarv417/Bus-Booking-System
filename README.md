# Bus Booking System

The Bus Booking System is a web-based application designed to facilitate the management and booking of bus seats. It caters to two distinct user roles: Admin and User, each with specific functionalities tailored to their needs. The system ensures a seamless experience for users to browse, book, and cancel bus seats while providing admins with robust tools to manage bus details efficiently.
[DEMO LINK](https://drive.google.com/file/d/1C542Ponsq1kK7aw83PEN8Vv8SfXBxQaZ/view?usp=sharing).

## Features

- **User/Admin Registration and Login**
- **Bus Booking for user**
- **Seat Availability Display with Color Codes**
  - Green: 60% full or less
  - Yellow: 60% - 90% full
  - Red: 90% - 100% full
- **Manage Bookings**
- **Admin Interface**
  - Add Buses
  - Manage Bookings

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Sanskarv417/Bus-Booking-System
    cd bus-booking-system
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - Ensure you have MySQL installed and running.
    - Create a new database:

        ```sql
        CREATE DATABASE bus_booking_system;
        ```

    - Update the database configuration in `app.py`:

        ```python
        DB_HOST = 'localhost'
        DB_USER = 'yourusername'
        DB_PASSWORD = 'yourpassword'
        DB_NAME = 'bus_booking_system'
        ```

5. **Run the application:**

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

- **User Interface:**
  - Register and login as a user.
  - Book and cancel a bus seat.
  - Check seat availability with color-coded indicators.
  - Manage your bookings.

- **Admin Interface:**
  - Login and register as an admin.
  - Add, update and delete new buses.
  - View and cancel bookings.
