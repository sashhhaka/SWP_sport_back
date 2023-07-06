from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404


from .models import Achievement, AchTeacher


# view for achievements
def index(request):
    teacher = AchTeacher.objects.get(user=request.user)
    achievement_list = Achievement.objects.filter(assigned_coaches__in=[teacher])
    context = {"achievement_list": achievement_list}
    return render(request, "ach_admin/index.html", context)


# test views
def detail(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    return render(request, "ach_admin/detail.html", {"achievement": achievement,
                                                     "subscribed_list": achievement.subscribed_students.all(),
                                                     "finished_list": achievement.finished_students.all()})

def design(request):
    return render(request, "ach_admin/menu.html")

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
