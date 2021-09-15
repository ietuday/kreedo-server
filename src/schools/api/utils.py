import datetime
import calendar


def month_calculation(start_date, months):
    # print(mont
    start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
    months = int(months)
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = min(start_date.day, calendar.monthrange(year, month)[1])
    print("*****************", datetime.date(year, month, day))
    return datetime.date(year, month, day)


def addYears(d, years):
    try:
        print("$$$$")
        # Return same day of the current year
        return d.replace(year=d.year + years)
    except ValueError:
        # If not same day, it will return other, i.e.  February 29 to March 1 etc.
        return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))
