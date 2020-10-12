import datetime


def age_in_years(from_date, to_date=None, leap_day_anniversary_Feb28=True):
    if to_date is None:
        to_date = datetime.date.today()
    age = to_date.year - from_date.year
    try:
        anniversary = from_date.replace(year=to_date.year)
    except ValueError:
        assert from_date.day == 29 and from_date.month == 2
        if leap_day_anniversary_Feb28:
            anniversary = datetime.date(to_date.year, 2, 28)
        else:
            anniversary = datetime.date(to_date.year, 3, 1)
    if to_date < anniversary:
        age -= 1
    return age
