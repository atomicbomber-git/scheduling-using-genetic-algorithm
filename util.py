from datetime import datetime

dayname_map = {
    "Sun": "Minggu",
    "Mon": "Senin",
    "Tue": "Selasa",
    "Wed": "Rabu",
    "Thu": "Kamis",
    "Fri": "Jum'at",
    "Sat": "Sabtu"
}


def format_time(dt: datetime):
    day_name = dayname_map[dt.strftime("%a")]

    return "({}) {} {}".format(
        dt.strftime("%w"),
        day_name,
        dt.strftime("%H:%M")
    )
