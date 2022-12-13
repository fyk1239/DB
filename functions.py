import psycopg2
import time
# 连接数据库


def connect_db():
    try:
        conn = psycopg2.connect(database="grade_system", user="postgres",
                                password="123", host="localhost", port="5432")
    except Exception as e:
        print("connect db error:", e)
    else:
        return conn
    return None

# 提交数据库语句并断开数据库连接


def close_db_connection(conn):
    conn.commit()
    conn.close()


# student
def search_stu(Cursor, num):  # 获取对应学号的学生的信息
    Cursor.execute("select * from Student where sno='"+num+"'")
    return Cursor.fetchone()


def update_password_for_student(Cursor, sno, newpassword):  # 修改学生密码
    Cursor.execute("update Student set Spasswd='" +
                   newpassword+"' where Sno='" + sno+"'")
    return Cursor.fetchone()


def get_grade(Cursor, sno):  # 查找学生的成绩
    Cursor.execute(
        "select Cno,Gscore from Student join grade on Student.Sno=Grade.Sno where Student.sno='"+sno+"'")
    return Cursor.fetchall()


def update_stu_info(Cursor, sno):  # 更新学生学分及平均成绩
    Cursor.execute(
        "select Course.Ccredit from Student,Grade,Course where Student.Sno=Grade.Sno and Grade.Cno=Course.Cno and where Student.Sno='"+sno+"'")
    credit = Cursor.fetchall()
    ammount = 0
    for c in credit:
        ammount += c[0]
    Cursor.execute("update Student set Stot_credit='" +
                   ammount+"' where Sno='" + sno+"'")

    Cursor.execute(
        "select Course.Ccredit from Student,Grade,Course where Student.Sno=Grade.Sno and Grade.Cno=Course.Cno and Student.Sno='"+sno+"' and Gscore>=60")
    credit = Cursor.fetchall()
    ammount = 0
    for c in credit:
        ammount += c[0]
    Cursor.execute("update Student set Scredit='" +
                   ammount+"' where Sno='" + sno+"'")

    Cursor.execute(
        "select Grade.Gscore from Student,Grade where Student.Sno=Grade.Sno and Student.Sno='"+sno+"'")
    grade = Cursor.fetchall()
    ammount = 0
    for g in grade:
        ammount += g[0]
    ammount /= len(grade)
    Cursor.execute("update Student set Savg='" +
                   ammount+"' where Sno='" + sno+"'")


def search_grade_from_id(Cursor, sno, cno):  # 通过课程号查找某学生的成绩
    Cursor.execute("select Cno,Gscore from Student join cno on Student.sno=Grade.sno where Student.Sno='" +
                   sno+"' and Cno like'%"+cno+"%'")
    return Cursor.fetchall()
    #Cursor.execute("select * from student natrual join grade where Sno='"+Sno+"' and Cno like '%"+Cno+"%'")


def search_grade_from_name(Cursor, sno, cname):  # 通过课程名查找某学生的成绩
    Cursor.execute("select Cno,Gscore from student join grade on student.sno=grade.sno where student.sno='" +
                   sno+"' and cname like'%"+cname+"%'")
    return Cursor.fetchall()


def get_course_announcement(Cursor, Cno):  # 查找课程公告
    Cursor.execute("select * from Announcement where Cno='"+Cno+"'")
    return Cursor.fetchall()


# teacher
def search_teacher_num(Cursor, num):  # 获取对应工号的教师的信息
    Cursor.execute("select * from teacher where tno='"+num+"'")
    return Cursor.fetchone()

# def update_password_for_teacher(Cursor,tno,newpassword):#修改教师密码
#   Cursor.execute("update teacher set Tpasswd='"+newpassword+"' where tno='"+ tno+"'")
#   return Cursor.fetchone()


def get_teacher_course(Cursor, tno):  # 查找教师教授的课
    Cursor.execute(
        "select * from teacher join course on teacher.tno=course.tno where teacher.tno='"+tno+"'")
    return Cursor.fetchall()


def publish_announcement(Cursor, Cno, announcement_content):  # 添加课程公告
    Cursor.execute("select count(*) from announcement ")
    Ano = Cursor.fetchone()[0]
    Ano = str(Ano)
    Cursor.execute("insert into announcement values('" +
                   Ano+"','"+announcement_content+"'")


def update_grade(Cursor, Sno, Cno, grade):  # 修改学生成绩
    Cursor.execute("update grade set Gscore="+grade +
                   " where Sno='"+Sno+"' and Cno='"+Cno+"'")


if __name__ == "__main__":
    # name="苹果"
    conn = connect_db()  # 连接数据库
    cur = conn.cursor()  # 创建会话
    # f_one=search_course_from_id(cur,'000000001','1')
    # print(f_one)
    # publish_announcement(cur,'000001',"测试公告")
    #print(time.asctime( time.localtime(time.time()) ))
    update_grade(cur, '000000001', '000001', '99')
