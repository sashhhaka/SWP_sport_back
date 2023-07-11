from django.urls import path

from . import views

app_name = "ach_admin"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("events/", views.events, name="events"),
    path("move/", views.move_element, name="menu2"),
]
