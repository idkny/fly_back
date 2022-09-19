from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = "fly"

urlpatterns = [
    path("", TemplateView.as_view(template_name="fly/index.html")),
    re_path(r"^countries$", views.Countries),
    re_path(r"^airlines$", views.Airlines),
    re_path(r"^airlines/(?P<pk>[0-9]+)$", views.MyAirlines),
    re_path(r"^flights$", views.Flights),
    re_path(r"^flights/(?P<pk>[0-9]+)$", views.MyFlights),
    re_path(r"^flightById/(?P<pk>[0-9]+)$", views.FlightByID),
    re_path(r"^filter$", views.FilterFlights),
    re_path(r"^tickets$", views.Tickets),
    re_path(r"^ticketsById/(?P<pk>[0-9]+)$", views.TicketsByID),
]
