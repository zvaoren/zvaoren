from dateutil.parser import parse
import datetime as dt

def year_from_date(date):
    dt = parse(date)
    return dt.date().year


def age_between_years(year_date, age):
    print("Years:", year_date, age)


def year_from_age(year_date, age):
    print("Years:", year_date, age, year_date - age)


date1 = "23-jun-1855"
age = "45"

year = year_from_date(date1)
birth_year = year_from_age(year, int(age))


