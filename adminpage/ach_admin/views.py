from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
import json

from .models import Achievement, AchTeacher


# view for achievements
def index(request):
    try:
        teacher = AchTeacher.objects.get(user=request.user)
    except AchTeacher.DoesNotExist:
        raise Http404("You do not have access to achievement functionality.")
    achievement_list = Achievement.objects.filter(assigned_coaches__in=[teacher])
    context = {"achievement_list": achievement_list}
    return render(request, "ach_admin/index.html", context)

def move_element(request):
    data = json.loads(request.body)
    ids = data.get('ids','')
    [object_id, element_id] = ids.split("/%/")
    my_object = get_object_or_404(Achievement, id=object_id)
    element_to_move = my_object.students.get(id=element_id)
    my_object.mark_student_as_finished(element_to_move)
    return HttpResponse("You're voting on question")

def move_element2(request):
    data = json.loads(request.body)
    ids = data.get('ids','')
    [object_id, element_id] = ids.split("/%/")
    my_object = get_object_or_404(Achievement, id=object_id)
    element_to_move = my_object.students.get(id=element_id)
    my_object.mark_student_as_sub(element_to_move)
    return HttpResponse("You're voting on question")

def events(request):
    teacher = AchTeacher.objects.get(user=request.user)
    achievement_list = Achievement.objects.all()
    context = {"achievement_list": achievement_list}
    return render(request, "ach_admin/events.html", context)


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
