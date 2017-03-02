import datetime

def ordinal(n):
    # Modified from http://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    ord_num = "%d%s" % (n, "tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    return ord_num

def validate_birth_year(year, min_age=0):
    max_year = datetime.datetime.now().year - min_age
    min_year = 1880
    try:
        year = int(year)
    except:
        return False
    if year > max_year or year < min_year:
        return False
    return year