from app01.models import Student, Teacher, Course, Grade, Announcement
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
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
    # 否则返回报错信息（errormsg）
    elif request.method == "POST":
        user = request.POST.get('user')
        pswd = request.POST.get('pswd')
        # 实现与数据库内密码判定
        students = Student.objects.all()
        for student in students:
            if student.Sno == user and student.Spasswd == pswd:
                request.session['curSno'] = user
                return redirect('/student.html')
            elif student.Sno == user and student.Spasswd != pswd:
                return render(request, 'loginstudent.html', {'msg': '密码错误'})
        return render(request, 'loginstudent.html', {'msg': '用户名错误'})


def loginteacher(request):
    # 若是get方法，则直接返回默认的登陆页面
    if request.method == "GET":
        return render(request, 'loginteacher.html')
    # 若是post方法，如果用户名密码正确，则重定向到index，
    # 否则返回报错信息页面（errormsg）
    elif request.method == "POST":
        user = request.POST.get('user')
        pswd = request.POST.get('pswd')
        # 实现与数据库内密码判定
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.Tno == user and teacher.Tpasswd == pswd:
                return redirect('/teacher.html')
        else:
            errormsg = "用户名或密码错误!"
            return render(request, 'loginteacher.html', {"errormsg": errormsg})


def student(req):
    template = loader.get_template('student.html')
    curSno = req.session.get('curSno')
    curUser = Student.objects.get(Sno=curSno)
    req.session['curUser'] = curUser
    # 传递当前学生的已选课程信息，如课程号、课程名、成绩、学分、课程属性等
    gradeList = Grade.objects.filter(Sno=curUser).all()
    tmpCourseList = Course.objects.all()
    courseList = {}
    for grade in gradeList:
        for course in tmpCourseList:
            if grade.Cno == course.Cno:
                courseList.append(course)
            if grade.Cno == course.Cno and grade.Gscore >= 60:
                curUser.Scredit += course.Ccredit
    content = {
        'curUser': curUser,
        'gradeList': gradeList,
        'courseList': courseList
    }
    return HttpResponse(template.render(content, req))


def studentsearch(req):
    curSno = req.session.get('curSno')
    curUser = Student.objects.get(Sno=curSno)
    gradeList = Grade.objects.filter(Sno=curSno).all()
    tmpCourseList = Course.objects.all()
    courseList = {}
    for grade in gradeList:
        for course in tmpCourseList:
            if grade.Cno == course.Cno:
                courseList.append(course)
    content = {
        'curUser': curUser,
        'gradeList': gradeList,
        'courseList': courseList
    }
    return render(req, 'studentsearch.html', content)


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
