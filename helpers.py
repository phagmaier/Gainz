from datetime import datetime
import config

def is_valid_date(date_str: str) -> bool:
    """Check if a string is a valid date in our format"""
    try:
        datetime.strptime(date_str, config.DATE_FORMAT)
        return True
    except ValueError:
        return False

def format_date(date_obj: datetime) -> str:
    """Format a datetime object to our standard string format"""
    return date_obj.strftime(config.DATE_FORMAT)

def parse_date(date_str: str) -> datetime:
    """Parse a date string to datetime object"""
    return datetime.strptime(date_str, config.DATE_FORMAT)

def get_days_between(date1_str: str, date2_str: str) -> int:
    """Calculate days between two date strings"""
    try:
        date1 = parse_date(date1_str)
        date2 = parse_date(date2_str)
        return abs((date2 - date1).days)
    except ValueError:
        return 0

def calculate_weight_change_rate(history: list) -> float:
    """Calculate average weight change per week from history"""
    if len(history) < 2:
        return 0.0
    
    try:
        first_weight, first_date = history[0]
        last_weight, last_date = history[-1]
        
        days = get_days_between(first_date, last_date)
        if days == 0:
            return 0.0
        
        weight_change = float(last_weight) - float(first_weight)
        weeks = days / 7.0
        
        return weight_change / weeks if weeks > 0 else 0.0
    except (ValueError, IndexError):
        return 0.0
