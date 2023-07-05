from django.urls import path

from . import views

app_name = "ach_admin"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),

]
