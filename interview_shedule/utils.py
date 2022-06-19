from datetime import datetime

def convert_to_24_format(timeIn12Hr):
  time_and_date = datetime.strptime(timeIn12Hr, '%I:%M %p')
  time_in_24_hr = datetime.strftime(time_and_date, '%H:%M')
  return time_in_24_hr