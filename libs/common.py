from datetime import datetime

def date_format(value, type_value, to_value):
    
    op = {
        'to_date' :datetime.strptime,
        'to_str': datetime.strftime
        
    }.get(to_value)
    
    if value:
        if str(type_value) == 'DATE':
            return op(value, '%Y-%m-%d')  
        elif str(type_value) == 'DATETIME':
            return op(value, '%Y-%m-%d %H:%M:%S')
        else:
            return value
    else:
        return value