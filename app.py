from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Viekhyat',
        database='flight_booking'
    )

@app.route('/api/flights', methods=['GET'])
def get_flights():
    conn = None
    cursor = None
    try:
        departure = request.args.get('departure')
        destination = request.args.get('destination')
        flight_date = request.args.get('date')

        app.logger.debug(f"Request received: departure={departure}, destination={destination}, date={flight_date}")

        if not all([departure, destination, flight_date]):
            return jsonify({"error": "Missing required parameters"}), 400
        
        try:
            flight_date = datetime.strptime(flight_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'yyyy-mm-dd'"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, airline, departure, destination, flight_date, 
               TIME_FORMAT(departure_time, '%H:%i') as departure_time,
               TIME_FORMAT(flight_duration, '%H:%i') as flight_duration,
               price
        FROM flights
        WHERE departure = %s 
        AND destination = %s 
        AND flight_date = %s
        """
        cursor.execute(query, (departure, destination, flight_date))
        flights = cursor.fetchall()

        if not flights:
            return jsonify({"error": "No flights found for the selected criteria"}), 404

        # Process the results
        for flight in flights:
            flight['flight_date'] = flight['flight_date'].strftime('%Y-%m-%d')
            # departure_time and flight_duration are already formatted by MySQL

        return jsonify(flights)

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/book', methods=['POST'])
def book_flight():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        required_fields = ['flightId', 'name', 'email', 'contact']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields for booking"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO need_booking (flight_id, name, email, contact)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['flightId'],
            data['name'],
            data['email'],
            data['contact']
        ))
        conn.commit()

        return jsonify({"message": "Booking successful!"}), 200

    except Exception as e:
        app.logger.error(f"Booking error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)