# Time to hours conversion helper function
def time_to_hours(timestr):
    try:
        h, m, s = map(int, timestr.split(":"))
        return h + (m / 60) + (s / 3600)
    except Exception:
        return None