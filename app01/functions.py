import psycopg2
import time
# 连接数据库


def connect_db():
    try:
        conn = psycopg2.connect(database="grade_system_DB", user="postgres",
                                password="fyk1239", host="localhost", port="5432")
    except Exception as e:
        print("connect db error:", e)
    else:
        print("connect db success!")
        return conn
    return None

# 提交数据库语句并断开数据库连接


def close_db_connection(conn):
    conn.commit()
    conn.close()


# app01_student
def search_stu(Cursor, Sno):  # 获取对应学号的学生的信息，修改完成
    Cursor.execute(
        "select * from public.app01_student where \"Sno\"='"+Sno+"'")
    return Cursor.fetchone()


def update_password_for_app01_student(Cursor, Sno, newpassword):  # 修改学生密码，修改完成
    Cursor.execute("update public.app01_student set \"Spasswd\"='" +
                   newpassword+"' where \"Sno\"='" + Sno+"'")


def get_grade(Cursor, Sno):  # 查找学生的成绩，修改完成
    Cursor.execute(
        "select app01_grade.\"Cno_id\", app01_grade.\"Gscore\" from public.app01_student join public.app01_grade on app01_student.\"Sno\"=app01_grade.\"Sno_id\" where app01_student.\"Sno\"='"+Sno+"'")
    return Cursor.fetchall()


def update_stu_info(Cursor, Sno):  # 更新学生学分及平均成绩，修改完成
    # 更新学生应修读学分
    Cursor.execute(
        "select \"Ccredit\" from public.app01_student,public.app01_grade,app01_course where app01_student.\"Sno\"=app01_grade.\"Sno_id\" and app01_grade.\"Cno_id\"=app01_course.\"Cno\" and app01_student.\"Sno\"='"+Sno+"'")
    credit = Cursor.fetchall()
    ammount = 0
    for c in credit:
        ammount += c[0]
    Cursor.execute("update public.app01_student set \"Stot_credit\"='" +
                   str(ammount)+"' where \"Sno\"='" + Sno+"'")

    # 更新学生已修读学分，分数高于60的科目才被承认
    Cursor.execute(
        "select \"Ccredit\" from public.app01_student,public.app01_grade,app01_course where app01_student.\"Sno\"=app01_grade.\"Sno_id\" and app01_grade.\"Cno_id\"=app01_course.\"Cno\" and app01_student.\"Sno\"='"+Sno+"' and \"Gscore\">=60")
    credit = Cursor.fetchall()
    ammount = 0
    for c in credit:
        ammount += c[0]
    Cursor.execute("update public.app01_student set \"Scredit\"='" +
                   str(ammount)+"' where \"Sno\"='" + Sno+"'")

    Cursor.execute(
        "select app01_grade.\"Gscore\" from public.app01_student,public.app01_grade where app01_student.\"Sno\"=app01_grade.\"Sno_id\" and app01_student.\"Sno\"='"+Sno+"'")
    grade = Cursor.fetchall()
    ammount = 0
    for g in grade:
        ammount += g[0]
    ammount /= len(grade)
    Cursor.execute("update public.app01_student set \"Savg\"='" +
                   str(ammount)+"' where \"Sno\"='" + Sno+"'")


def search_grade_from_id(Cursor, Sno, Cno):  # 通过课程号查找某学生的成绩，修改完成
    Cursor.execute("select public.app01_grade.\"Cno_id\", public.app01_grade.\"Gscore\" from public.app01_student join public.app01_grade on app01_student.\"Sno\"=app01_grade.\"Sno_id\" where app01_student.\"Sno\"='" +
                   Sno+"' and \"Cno_id\" like'%"+Cno+"%'")
    return Cursor.fetchall()
    #Cursor.execute("select * from app01_student natrual join grade where Sno='"+Sno+"' and Cno like '%"+Cno+"%'")


def search_grade_from_name(Cursor, Sno, Cname):  # 通过课程名查找某学生的成绩
    Cursor.execute("select \"Cno_id\",\"Gscore\" from public.app01_student join public.app01_grade on app01_student.\"Sno\"=app01_grade.\"Sno\" where \"app01_student.Sno\"='" +
                   Sno+"' and \"Cname\" like'%"+Cname+"%'")
    return Cursor.fetchall()


def get_app01_course_announcement(Cursor, Cno):  # 通过课程号查找课程公告
    Cursor.execute(
        "select * from public.app01_announcement where \"Cno\"='"+Cno+"'")
    return Cursor.fetchall()


# teacher
def search_teacher_num(Cursor, Tno):  # 获取对应工号的教师的信息
    Cursor.execute(
        "select * from public.app01_teacher where \"Tno\"='"+Tno+"'")
    return Cursor.fetchone()

# def update_password_for_teacher(Cursor,tno,newpassword):#修改教师密码
#   Cursor.execute("update teacher set Tpasswd='"+newpassword+"' where tno='"+ tno+"'")
#   return Cursor.fetchone()


def get_teacher_app01_course(Cursor, Tno):  # 查找教师教授的课
    Cursor.execute(
        "select * from public.app01_teacher join public.app01_course on \"app01_teacher.Tno\"=\"app01_course.Tno\" where \"app01_teacher.Tno\"='"+Tno+"'")
    return Cursor.fetchall()


def publish_announcement(Cursor, Cno, announcement_content):  # 添加课程公告
    Cursor.execute("select \"count(*)\" from public.app01_announcement ")
    Ano = Cursor.fetchone()[0]
    Ano = str(Ano)
    Cursor.execute("insert into public.app01_announcement values('" +
                   Ano+"','"+announcement_content+"'")


def update_grade(Cursor, Sno, Cno, grade):  # 修改学生成绩，修改成功
    Cursor.execute("update public.app01_grade set \"Gscore\"="+grade +
                   " where \"Sno_id\"='"+Sno+"' and \"Cno_id\"='"+Cno+"'")


if __name__ == "__main__":
    conn = connect_db()  # 连接数据库
    cur = conn.cursor()  # 创建会话
    # print(search_stu(cur, '00001'))
    # print(get_grade(cur, '00002'))
    # f_one=search_app01_course_from_id(cur,'000000001','1')
    # print(f_one)
    # publish_announcement(cur,'000001',"测试公告")
    # print(time.asctime( time.localtime(time.time()) ))
    update_grade(cur, '00001', '20001', '99')
    update_stu_info(cur, '00001')
    # print(update_stu_info(cur, '00001'))
    # print(search_grade_from_id(cur, '00001', '20001'))
    print(search_grade_from_name(cur, '00001', '计算机网络'))
    close_db_connection(conn)  # 关闭数据库连接
