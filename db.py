import mysql.connector
import os
import logging
import datetime
from dotenv import load_dotenv
from typing import Dict, Optional

if not os.getenv("DB_HOST"):
    load_dotenv()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_db_connection():
    #establish db connection
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "3306"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "faculty_schedule"),
            connect_timeout=10
        )
        return conn if conn.is_connected() else None
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return None

def get_faculty_info(faculty_name: str, db) -> Optional[Dict]:
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, staffroom FROM faculty WHERE name = %s", (faculty_name,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return None

def get_faculty_schedule(faculty_id: int, day: str, period: int, period_type: Optional[str], db) -> Optional[Dict]:
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT subject, class, room_code, period_type
            FROM timetable
            WHERE faculty_id = %s AND day = %s AND period = %s
            ORDER BY FIELD(period_type, 'regular', 'firstyear')  -- Prioritize 'regular' if both exist
            LIMIT 1
        """
        cursor.execute(query, [faculty_id, day, period])
        result = cursor.fetchone()

        if not result:
            logger.error(f"No schedule found for faculty_id={faculty_id}, day={day}, period={period}")

        return result
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        return None
def determine_current_period():
    now = datetime.datetime.now()
    hour, minute = now.hour, now.minute
    # Define period mappings
    if 9 <= hour < 10:
        return 1, "regular"
    elif 10 <= hour < 11:
        return 2, "regular"
    elif 11 <= hour < 12 or (hour == 12 and minute <= 10):
        return 3, "regular"
    elif (hour == 12 and minute >= 10) or (hour == 13 and minute <= 10):
        return 4, "firstyear"  # First-year special case
    elif 13 <= hour < 14:
        return 4, "regular"
    elif 14 <= hour < 15:
        return 5, "regular"
    elif 15 <= hour < 16:
        return 6, "regular"

    return None, None  # No active period
