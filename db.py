# db.py
import mysql.connector
import os
import logging
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables
if not os.getenv("DB_HOST"):
    load_dotenv()

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "3306"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "faculty_schedule"),
            connect_timeout=10
        )
        if conn.is_connected():
            return conn
        else:
            logger.error("Database connection failed.")
            return None
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return None

def get_faculty_info(faculty_name: str, db: mysql.connector.connection) -> Optional[Dict]:
    """Retrieve faculty information from the database."""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, staffroom FROM faculty WHERE name = %s", (faculty_name,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return None

def get_current_faculty_location(faculty_id: int, db: mysql.connector.connection) -> Optional[Dict]:
    """Get current faculty location (class or staffroom)."""
    cursor = db.cursor(dictionary=True)
    current_time = datetime.datetime.now().time()
    
    # Period mapping
    periods = [
        (9, 10, 1), (10, 11, 2), (11, 12, 3),
        (12, 13, 4), (13, 14, 4), (14, 15, 5), (15, 16, 6)
    ]
    
    # Find current period
    current_period = next(
        (p for (start, end, p) in periods 
         if start <= current_time.hour < end), None
    )
    
    if not current_period:
        return None
    
    # Get current class information
    cursor.execute("""
        SELECT t.subject, t.class, t.room_code, t.period_type
        FROM timetable t
        WHERE t.faculty_id = %s AND t.day = %s AND t.period = %s
    """, (faculty_id, datetime.datetime.today().strftime('%A'), current_period))
    
    return cursor.fetchone()


