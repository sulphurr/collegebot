import re
import logging
from datetime import datetime, timedelta
from db import get_db_connection, get_faculty_info, get_faculty_schedule, determine_current_period

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def clean_query(query: str) -> str:
    return re.sub(r'\b(Ms\.|Mr\.|Dr\.|Prof\.)\s*', '', query, flags=re.IGNORECASE).strip()

def extract_faculty_details(query: str, faculty_list: list) -> dict:
    try:
        query = clean_query(query.lower())
        faculty_name = next((name for name in faculty_list if name.lower() in query), None)
        if not faculty_name:
            return {}
        
        is_staffroom_query = "staffroom" in query
        
        if "tomorrow" in query:
            day = (datetime.today() + timedelta(days=1)).strftime("%A")
        else:
            day_match = re.search(r'\b(monday|tuesday|wednesday|thursday|friday)\b', query)
            day = day_match.group(0).capitalize() if day_match else datetime.today().strftime("%A")
        
        period_match = re.search(r'period\s*(\d+)|p\s*(\d+)', query)
        period = period_match.group(1) or period_match.group(2) if period_match else "current"
        
        return {"name": faculty_name, "day": day, "period": period, "is_staffroom_query": is_staffroom_query}
    except Exception as e:
        logger.error(f"Error extracting faculty details: {e}")
        return {}

def handle_faculty_query(query: str, db):
    db = get_db_connection()
    if not db:
        logger.error("Database connection failed.")
        return "Database connection failed."
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT name FROM faculty")
            faculty_list = [row[0] for row in cursor.fetchall() if row[0]]
        details = extract_faculty_details(query, faculty_list)
        if not details:
            return "I couldn't understand which faculty member you're asking about."      
        faculty_name = details["name"]
        faculty_info = get_faculty_info(faculty_name, db)
        if not faculty_info:
            return f"Faculty details for {faculty_name} are not available."
        
        if details["is_staffroom_query"]:
            staffroom = faculty_info.get("staffroom", "Staffroom information not available")
            return f"{faculty_name}'s staffroom is {staffroom}."
        
        period = details["period"]
        period_type = "regular"
        
        if period == "current":
            period, period_type = determine_current_period()
            if not period:
                return f"{faculty_name} is not teaching right now."
        
        schedule = get_faculty_schedule(faculty_info["id"], details["day"], period, period_type, db)
        
        return (
            f"{faculty_name} teaches {schedule['subject']} for {schedule['class']} in {schedule['room_code']} "
            f"during period {period}." if schedule else 
            f"{faculty_name} has no scheduled classes during period {period} on {details['day']}."
        )
    except Exception as e:
        logger.error(f"Error handling faculty query: {e}")
        return "An error occurred while processing your request."
    finally:
        db.close()
