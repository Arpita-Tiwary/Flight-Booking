import mysql.connector
import logging

# Enable logging for better debugging
logging.basicConfig(level=logging.DEBUG)

# MySQL connection setup
def get_db_connection():
    try:
        # Establish the connection to the MySQL server
        conn = mysql.connector.connect(
            host='localhost',  # Change as necessary
            user='root',
            password='Viekhyat',
            database='flight_booking'  # Database used for fetching flight data
        )

        # Test the connection by running a simple query
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        cursor.close()
        conn.close()

        if databases:
            logging.info("Connected to MySQL server. Databases: %s", databases)
        else:
            logging.error("Failed to fetch databases.")

    except mysql.connector.Error as err:
        # Log the error if connection fails
        logging.error(f"Error: {err}")

# Check connection
get_db_connection()
