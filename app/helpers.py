def convert_to_datetime(date): # Converts dates with the format "Year-Month-Day" to "Year,Month,Day"
    split_date = date.split("-")
    return "{year}, {month}, {day}".format(year=split_date[0], month=split_date[1], day=split_date[2])