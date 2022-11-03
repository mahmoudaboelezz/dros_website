from django.urls import path

from . import views
from .views.other_views import member_join,delete_event

app_name = "calendarapp"


urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path("", views.CalendarView.as_view(), name="calendars"),
    path("event/new/", views.create_event, name="event_new"),
    path("event/delete/", delete_event, name="delete_event"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path("add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"),
    path("event/<int:pk>/remove",views.EventMemberDeleteView.as_view(),name="remove_event",),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/",views.RunningEventsListView.as_view(),name="running_events",),
    path("upcoming-event-list/",views.UpcomingEventsListView.as_view(),name="upcoming_events",),
    path("member_join/<int:event_id>", member_join, name="member_join"),
]
