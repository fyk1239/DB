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
                request.session['curTno'] = user
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
    # 更新学生学分及平均成绩
    func.update_stu_info(cur, curSno)
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
    template = loader.get_template('teacher.html')
    curTno = req.session.get('curTno')
    req.session['curTno'] = curTno
    # 连接数据库
    conn = func.connect_db()
    cur = conn.cursor()
    # 传递当前教师在数据库中的信息
    curTeacher = func.search_teacher_num(cur, curTno)
    curTeacherName = curTeacher[1]
    req.session['curTeacherName'] = curTeacherName
    # 接收用户输入的课程号
    courseNo = req.POST.get('courseNo')
    if courseNo != None:
        req.session['courseNo'] = courseNo
        return redirect('/coursesearch.html')
    # 根据教师号查询教师所教课程信息
    curCourse = func.get_teacher_course(cur, curTno)
    # 根据课程号查询教师所教课程的公告信息
    curCourseNo = []
    for c in curCourse:
        curCourseNo.append(c[4])
    # 按照课程号查询课程公告内容并存入列表
    curAnnouncement = []
    for c in curCourseNo:
        tmpcourse = func.get_course_announcement(cur, c)
        curAnnouncement.append(tmpcourse)
    # 传递上下文
    content = {
        'curTno': curTno,
        'curTeacherName': curTeacherName,
        'curCourse': curCourse,
        'curAnnouncement': curAnnouncement,
    }
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))

# 暂时不用


def teachersearch(req):
    template = loader.get_template('teachersearch.html')
    # 连接数据库
    conn = func.connect_db()
    cur = conn.cursor()
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))


def coursesearch(req):
    template = loader.get_template('coursesearch.html')
    # 接收当前教师姓名
    curTeacherName = req.session.get('curTeacherName')
    req.session['curTeacherName'] = curTeacherName
    # 接收用户输入的课程号
    courseNo = req.session.get('courseNo')
    req.session['courseNo'] = courseNo
    # 接收用户输入的学号
    studentNo = req.POST.get('studentNo')
    if studentNo != None:
        req.session['studentNo'] = studentNo
        return redirect('/entry.html')
    # 连接数据库
    studentNo = req.session.get('studentNo')
    conn = func.connect_db()
    cur = conn.cursor()
    curGrade = []
    # 根据课程号查询选课学生
    if courseNo != None:
        curStudent = func.get_course_student(cur, courseNo)
        for s in curStudent:
            # 根据选课学生号查询学生成绩
            curStudentNo = s[0]
            curGrade.append(func.search_grade_from_id(
                cur, curStudentNo, courseNo))
    # 传递上下文
    content = {
        'curTeacherName': curTeacherName,
        'curGrade': curGrade,
    }
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))


def send(req):
    template = loader.get_template('send.html')
    return HttpResponse(template.render(content, req))


def show(req):
    template = loader.get_template('show.html')
    curTno = req.session.get('curTno')
    # 连接数据库
    conn = func.connect_db()
    cur = conn.cursor()
    # 传递当前教师在数据库中的信息
    curTeacher = func.search_teacher_num(cur, curTno)
    # 根据教师号查询教师所教课程信息
    curCourse = func.get_teacher_course(cur, curTno)
    # 根据课程号查询教师所教课程的公告信息
    curCourseNo = []
    for c in curCourse:
        curCourseNo.append(c[4])
    # 按照课程号查询课程公告内容并存入列表
    curAnnouncement = []
    for c in curCourseNo:
        tmpcourse = func.get_course_announcement(cur, c)
        curAnnouncement.append(tmpcourse)
    # 传递上下文
    content = {
        'curTno': curTno,
        'curTeacherName': curTeacher[1],
        'curAnnouncement': curAnnouncement
    }
    # 关闭数据库连接
    func.close_db_connection(conn)
    return HttpResponse(template.render(content, req))


def change(req):
    return render(req, 'change.html')


def entry(req):
    # 接收当前教师姓名
    curTeacherName = req.session.get('curTeacherName')
    req.session['curTeacherName'] = curTeacherName
    # 接收用户输入的课程号
    courseNo = req.session.get('courseNo')
    req.session['courseNo'] = courseNo
    # 接收用户输入的学号
    studentNo = req.session.get('studentNo')
    req.session['studentNo'] = studentNo
    # 接收用户输入的平时成绩、考勤成绩和期末成绩
    usual = req.POST.get('usual')
    attendance = req.POST.get('attendance')
    final = req.POST.get('final')
    print(usual, attendance, final)
    # 计算新成绩
    if usual != None and attendance != None and final != None:
        newScore = str(int(usual) * 0.4 + int(attendance)
                       * 0.1 + int(final) * 0.5)
        # 连接数据库
        conn = func.connect_db()
        cur = conn.cursor()
        curGrade = []
        # 根据学号和课程号更新学生成绩
        if studentNo != None and courseNo != None:
            func.update_grade(cur, studentNo, courseNo, newScore)
        # 关闭数据库连接
        func.close_db_connection(conn)
        return redirect('/teacher.html')
    return render(req, 'entry.html')


def password(req):
    return render(req, 'password.html')


def req(request):
    # return HttpResponse("dsa")
    print(request.method)
    print(request.GET)
    print(request.POST)
    return HttpResponse("success")
