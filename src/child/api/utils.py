from datetime import datetime
from django.core.exceptions import ValidationError


""" Calculate Working Days """
def calculate_working_days(start_date, end_date):
    try:
        working_days = end_date - start_date
        return working_days.days
    except Exception as ex:
        raise ValidationError(ex)

""" Calculate Blocks """
def calculate_blocks(working_days):
    try:
        return round(working_days/20)
    except Exception as ex:
        raise ValidationError(ex)
    