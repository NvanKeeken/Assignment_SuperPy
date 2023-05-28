
from advance import get_date_Format

def validation_check_date(expected_date_format, date):
    date_format = get_date_Format(date)
    is_date_valid = False
    if date_format == expected_date_format:
           is_date_valid += True
    else:
        is_date_valid += False
        raise ValueError(f"Date needs to be formatted as {expected_date_format}")
    return is_date_valid
    
