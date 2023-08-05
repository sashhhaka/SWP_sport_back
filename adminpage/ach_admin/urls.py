from django.urls import path

from . import views

app_name = "ach_admin"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("events/", views.events, name="events"),
    path("move/", views.move_element, name="menu2"),
    path("move2/", views.move_element2, name="menu3"),
    path("sub_students_list/", views.sub_students_list, name="menu4"),
    path("fin_students_list/", views.fin_students_list, name="menu5"),
]
