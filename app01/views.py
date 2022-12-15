from app01.models import Student, Teacher, Course, Grade, Announcement
import app01.functions as func
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
    # 连接数据库
    conn = func.connect_db()
    cur = conn.cursor()
    # 传递当前学生在数据库中的信息
    curStudent = func.search_stu(cur, curSno)
    curCourse = func.search_course(cur, curSno)
    curCourseNo = []
    for c in curCourse:
        curCourseNo.append(c[1])
    # 按照课程号查询课程公告内容并存入列表
    curAnnouncement = []
    for i in range(len(curCourseNo)):
        tmpcourse = func.get_course_announcement(cur, curCourseNo[i])
        curAnnouncement.append(tmpcourse)
    content = {
        'curSno': curSno,
        'curStudentName': curStudent[2],
        'curStudentDept': curStudent[3],
        'curStudentTotalCredit': curStudent[4],
        'curStudentCredit': curStudent[5],
        'curStudentAvgScore': curStudent[6],
        'curAnnouncement': curAnnouncement,
    }
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))


def studentsearch(req):
    template = loader.get_template('studentsearch.html')
    curSno = req.session.get('curSno')
    # 连接数据库
    conn = func.connect_db()
    cur = conn.cursor()
    # 传递当前学生在数据库中的信息
    curStudent = func.search_stu(cur, curSno)
    curCourse = func.search_course(cur, curSno)
    curCourseNo = []
    for c in curCourse:
        curCourseNo.append(c[1])
    # 按照课程号查询课程公告内容并存入列表
    curAnnouncement = []
    for i in range(len(curCourseNo)):
        tmpcourse = func.get_course_announcement(cur, curCourseNo[i])
        curAnnouncement.append(tmpcourse)
    # 若是post方法，则接收用户输入的筛选条件
    if req.method == "POST":
        courseName = req.POST.get('coursename')
        courseNo = req.POST.get('coursenum')
        courseProperty = req.POST.get('courseattribute')
        courseLevel = req.POST.get('courselevel')
        # 筛选对应的的课程信息
        if courseName != '':
            for c in curCourse:
                if courseName != c[0]:
                    curCourse.remove(c)
        if courseNo != '':
            for c in curCourse:
                if courseNo != c[1]:
                    curCourse.remove(c)
        if courseProperty != '':
            for c in curCourse:
                if courseProperty != c[3]:
                    curCourse.remove(c)
        if courseLevel != '':
            for c in curCourse:
                if courseLevel != c[5]:
                    curCourse.remove(c)
    # 根据输入的课程号查询课程信息，如课程名、学分、课程属性、课程分数、分数等级
    content = {
        'curSno': curSno,
        'curStudentName': curStudent[2],
        'curStudentDept': curStudent[3],
        'curStudentTotalCredit': curStudent[4],
        'curStudentCredit': curStudent[5],
        'curStudentAvgScore': curStudent[6],
        'curAnnouncement': curAnnouncement,
        'curCourse': curCourse,
    }
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))


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
