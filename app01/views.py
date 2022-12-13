# from unicodedata import name

# from sympy import re
from app01.models import Student, Teacher, Course, Grade, Announcement
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
# Create your views here.


def login(request):
    # 若是get方法，则直接返回默认的登陆页面
    if request.method == "GET":
        return render(request, 'login.html')


def loginstudent(request):
    # 若是get方法，则直接返回默认的登陆页面
    if request.method == "GET":
        return render(request, 'loginstudent.html')
    # 若是post方法，如果用户名密码正确，则重定向到index，
    # 否则返回报错信息页面（errormsg）
    elif request.method == "POST":
        user = request.POST.get('user')
        pswd = request.POST.get('pswd')
        if user == "admin" and pswd == "123":
            return redirect('/student.html')
        else:
            errormsg = "用户名或密码错误!"
            return render(request, 'loginstudent.html', {"errormsg": errormsg})


def loginteacher(request):
    # 若是get方法，则直接返回默认的登陆页面
    if request.method == "GET":
        return render(request, 'loginteacher.html')
    # 若是post方法，如果用户名密码正确，则重定向到index，
    # 否则返回报错信息页面（errormsg）
    elif request.method == "POST":
        user = request.POST.get('user')
        pswd = request.POST.get('pswd')
        # 未实现与判定
        if user == "admin" and pswd == "123":
            return redirect('/teacher.html')
        else:
            errormsg = "用户名或密码错误!"
            return render(request, 'loginteacher.html', {"errormsg": errormsg})


def student(req):
    return render(req, 'student.html')


def studentsearch(req):
    return render(req, 'studentsearch.html')


def teacher(req):
    return render(req, 'teacher.html')


def teachersearch(req):
    return render(req, 'teachersearch.html')


def coursesearch(req):
    return render(req, 'coursesearch.html')


def send(req):
    return render(req, 'send.html')


def show(req):
    return render(req, 'show.html')


def change(req):
    return render(req, 'change.html')


def entry(req):
    return render(req, 'entry.html')


def password(req):
    return render(req, 'password.html')


def req(request):
    # return HttpResponse("dsa")
    print(request.method)
    print(request.GET)
    print(request.POST)
    return HttpResponse("success")