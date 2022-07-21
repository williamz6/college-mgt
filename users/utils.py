from datetime import datetime

def generate_id():
    
    year = datetime.now()
    year = year.strftime('%y')
    college = 'TCH'
    col_num = '01'
    staff_no = 1
    id=f'{year}/{college.upper()}{col_num}/{str(staff_no).zfill(3)}'
    return id

generate_id()