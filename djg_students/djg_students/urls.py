"""
URL configuration for djg_students project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from students.views import *

urlpatterns = [
    path('', get_homepage, name="homepage"),
    path('students/', get_all_students, name="student_list"),
    path('students/add/', student_details, name="add_student"),
    path('students/add/<int:pk>', student_details, name="edit_student"),
    path('lectures/', get_all_lectures, name="lecture_list"),
    path('lectures/add/', lecture_details, name="add_lecture"),
    path('lectures/add/<int:pk>', lecture_details, name="edit_lecture"),
    path('lectures/add/<int:pk>/delete/', delete_lecture, name="delete_lecture"),
    path('admin/', admin.site.urls),
]
