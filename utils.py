from datetime import datetime

def format_date(date_str):
    """Converts a date string from 'YYYY-MM-DDTHH:MM:SS.sssZ' to 'DD/MM/YYYY HH:MM:SS' format."""

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%d/%m/%Y %H:%M:%SZ")
    
    except ValueError:
        return date_str 