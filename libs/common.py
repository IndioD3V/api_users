from datetime import date, datetime

def date_format_date(value, type_value):

    if str(type_value) == 'DATE':
        return datetime.strptime(value, '%Y-%m-%d') 
    elif str(type_value) == 'DATETIME':
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    else:
        return value
    
def date_format_str(value, type_value):

    if str(type_value) == 'DATE':
        return datetime.strftime(value, '%Y-%m-%d') 
    elif str(type_value) == 'DATETIME':
        return datetime.strftime(value, '%Y-%m-%d %H:%M:%S') if value else value
    else:
        return value