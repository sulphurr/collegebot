# faculty.py
from datetime import datetime
from typing import Dict, Optional
import re

def extract_faculty_details(query: str) -> Optional[Dict]:
    """Extract faculty name and other details from the query."""
    try:
        # Remove common words and clean the query
        query = query.lower()
        query = re.sub(r'\b(where|is|in|at|what|which|find)\b', '', query)
        query = query.strip()
        
        # Look for faculty name (assuming it's the first proper noun)
        words = query.split()
        faculty_name = None
        
        for i, word in enumerate(words):
            if word.istitle():
                faculty_name = word
                break
        
        if not faculty_name:
            return None
            
        # Extract day and period if present
        day_match = re.search(r'\b(monday|tuesday|wednesday|thursday|friday)\b', query)
        day = day_match.group(1).capitalize() if day_match else None
        
        period_match = re.search(r'\b(period|p)\s*(\d)\b', query)
        period = period_match.group(2) if period_match else None
        
        return {
            "name": faculty_name,
            "day": day,
            "period": period if period else "current"
        }
    except Exception as e:
        logger.error(f"Error extracting faculty details: {e}")
        return None

def handle_faculty_query(query: str, db: mysql.connector.connection) -> str:
    """Handle queries about faculty location and schedule."""
    details = extract_faculty_details(query)
    if not details:
        return "I couldn't understand which faculty member you're asking about."
    
    faculty_name = details.get("name")
    faculty_info = get_faculty_info(faculty_name, db)
    if not faculty_info:
        return f"I couldn't find information on {faculty_name}."
    
    if details.get("period") == "current":
        current_location = get_current_faculty_location(faculty_info["id"], db)
        if current_location:
            return (f"{faculty_name} is currently teaching {current_location['subject']} "
                   f"for {current_location['class']} in {current_location['room_code']}.")
        return (f"{faculty_name} is currently not teaching. You may find them in "
               f"staffroom {faculty_info['staffroom']}.")
    
    # Handle specific period queries
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT subject, class, room_code, period_type
        FROM timetable
        WHERE faculty_id = %s AND day = %s AND period = %s
    """, (faculty_info["id"], details.get("day"), details.get("period")))
    
    row = cursor.fetchone()
    if row:
        return (f"{faculty_name} teaches {row['subject']} for {row['class']} "
                f"in {row['room_code']} during period {details.get('period')}.")
    return (f"{faculty_name} does not have a scheduled class during "
            f"period {details.get('period')} on {details.get('day')}.")