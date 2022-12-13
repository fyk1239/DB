"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path("", views.login),
    path("login.html/", views.login),
    path("loginstudent.html/", views.loginstudent),
    path("loginteacher.html/", views.loginteacher),

    path('student.html/', views.student),
    path('studentsearch.html/', views.studentsearch),

    path('teacher.html/', views.teacher),
    path('teachersearch.html/', views.teachersearch),

    path('coursesearch.html/', views.coursesearch),
    path('send.html/', views.send),
    path('show.html/', views.show),
    path('change.html/', views.change),
    path('entry.html/', views.entry),
    path('password.html/', views.password)


    # path('person_query_model/',views.person_query_model)

    # path("admin/", admin.site.urls),
]
