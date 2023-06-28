from django.urls import path

from . import views

app_name = "ach_admin"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("design/", views.design, name="menu"),


    # test pages
    # ex: /polls/5/
    path("<int:achievement_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

]
