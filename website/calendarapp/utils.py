# calendarapp/utils.py
from calendar import HTMLCalendar
from .models import Event
from django.utils.translation import gettext_lazy as _

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        if day == 0:
            return "<td class='table-active'></td>"
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            startday = 6
            endday = 10
            # show from day 6 to day 13
            if d >= startday and d <= endday:
                week += self.formatday(d, events)
            else:
                if d>endday:
                    break
                week += self.formatday(0, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )
        cal = (
            '<table border="1" style="empty-cells:hide;" class="table  calendar">\n'
        )  # noqa
        
        # show period that i can choose 
        
        cal += (
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):

            cal += f"{self.formatweek(week, events)}\n"
             
            # print(week[0][:])
            # cal += f"{self.formatweek(week, events)}\n"
        return _(cal)
