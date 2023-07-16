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
    ids = data.get('ids', '')
    [object_id, element_id] = ids.split("/%/")
    my_object = get_object_or_404(Achievement, id=object_id)
    element_to_move = my_object.students.get(id=element_id)
    my_object.mark_student_as_finished(element_to_move)
    return HttpResponse("You're voting on question")


def sub_students_list(request):
    data = json.loads(request.body)
    ids = data.get('ids', '')
    [object_id, name] = ids.split("/%/")
    print(object_id,name)
    var = str(get_object_or_404(Achievement, id=object_id).subscribed_students()).split('AchStudent: ')
    print("sub = ")
    print(var)
    v = ''
    for i in range(1, len(var)):
        v += '<div class="students_list">' + '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + '<span style="display: inline-block; width: 80%; vertical-align: middle;">' + var[i].split('>')[0] + '</span>' + '<input class="button_for_students" id="lbutton' + name + str(i - 1) + '" type="checkbox" style="display: inline-block; width: 20%; vertical-align: middle;">' + '</p>' + '</div>';
    if v == '':
        v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No subscribed students</p>';
    return HttpResponse(v)

def fin_students_list(request):
    data = json.loads(request.body)
    ids = data.get('ids', '')
    [object_id, name] = ids.split("/%/")
    print(object_id,name)
    var = str(get_object_or_404(Achievement, id=object_id).finished_students()).split('AchStudent: ')
    print("fin = ")
    print(var)
    v = ''
    for i in range(1, len(var)):
        v += '<div class="students_list">' + '<p style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">' + '<span style="display: inline-block; width: 80%; vertical-align: middle;">' + var[i].split('>')[0] + '</span>' + '<input class="button_for_students" id="rbutton' + name + str(i - 1) + '" type=checkbox checked=checked style="display: inline-block; width: 20%; vertical-align: middle;">' + '</p>' + '</div>';
    if v == '':
        v = '<p class="students_list" style="color: black; font-size: 15px; font-family: -apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'Noto Sans\',sans-serif,\'Apple Color Emoji\',\'Segoe UI Emoji\',\'Segoe UI Symbol\',\'Noto Color Emoji\';">No finished students</p>';
    return HttpResponse(v)

def move_element2(request):
    data = json.loads(request.body)
    ids = data.get('ids', '')
    [object_id, element_id] = ids.split("/%/")
    my_object = get_object_or_404(Achievement, id=object_id)
    element_to_move = my_object.students.get(id=element_id)
    my_object.mark_student_as_subscribed(element_to_move)
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
