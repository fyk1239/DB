from django.db import models

# Create your models here.
# 成绩管理系统数据库设计
# 学生表：Sno,Spasswd,Sname,Sdept,Stot_credit,Scredit,Savg
# 教师表：Tno,Tname,Tdept,TCno
# 课程表：Cno,Cname,Ccredit
# 课程公告表：Ano,ACno,Acontent
# 成绩表：GSno,GCno,Grade

# 字段值与选项参考:
# https://docs.djangoproject.com/zh-hans/4.1/ref/models/fields/#field-types


# 学生
class Student(models.Model):
    # 学生学号，主码，不可为空，不可重复
    Sno = models.CharField(primary_key=True, max_length=5,
                           unique=True, null=False, default='0')
    # 学生密码
    Spasswd = models.CharField(max_length=20)
    # 学生姓名
    Sname = models.CharField(max_length=20)
    # 学生系别
    Sdept = models.CharField(max_length=20)
    # 学生总学分
    Stot_credit = models.DecimalField(
        max_digits=3, decimal_places=0, default=0)
    # 学生已修读学分
    Scredit = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    # 学生平均成绩
    Savg = models.DecimalField(max_digits=3, decimal_places=0, default=0)

# 教师


class Teacher(models.Model):
    # 教师工号，主码，不可为空，不可重复
    Tno = models.CharField(primary_key=True, max_length=5,
                           unique=True, null=False, default='0')
    # 教师密码
    Tpasswd = models.CharField(max_length=20, default='123')
    # 教师姓名
    Tname = models.CharField(max_length=20)
    # 教师系别
    Tdept = models.CharField(max_length=20)

# 课程


class Course(models.Model):
    # 课程号，主码，不可为空，不可重复
    Cno = models.CharField(primary_key=True, max_length=10,
                           unique=True, null=False, default='0')
    # 课程名
    Cname = models.CharField(max_length=20)
    # 课程学分
    Ccredit = models.DecimalField(max_digits=1, decimal_places=0)
    # 课程属性，选修或必修
    Cproperty = models.CharField(max_length=20, default='')
    # 上课教师工号，外码约束
    Tno = models.ForeignKey('Teacher', to_field='Tno',
                            on_delete=models.CASCADE, null=True)

# 成绩


class Grade(models.Model):
    # 成绩号，主码，不可为空，不可重复
    Gno = models.CharField(primary_key=True, max_length=10,
                           unique=True, null=False, default='0')
    # 学生学号，外码约束
    Sno = models.ForeignKey('Student', to_field='Sno',
                            on_delete=models.CASCADE, null=True)
    # 课程号，外码约束
    Cno = models.ForeignKey('Course', to_field='Cno',
                            on_delete=models.CASCADE, null=True)
    # 课程成绩
    Gscore = models.DecimalField(max_digits=3, decimal_places=0, default=0)

# 公告


class Announcement(models.Model):
    # 公告号，主码，不可为空，不可重复
    Ano = models.CharField(primary_key=True, max_length=5, serialize=False)
    # 公告所属课程，外码约束
    Cno = models.ForeignKey('Course', to_field='Cno',
                            on_delete=models.CASCADE, null=True)
    # 公告内容
    Acontent = models.CharField(max_length=200)
