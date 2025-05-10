from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from students.forms import *
from students.models import *

def get_homepage(request):
    return render(request, "students/homepage.html")
# Create your views here.
def get_all_students(request):
    students = Student.objects.all().order_by("lname", "fname")

    return render(request, "students/student_list.html", {"page_title": "Studenten",
                                                          "students": students})


def get_all_lectures(request):
    lectures = Lecture.objects.all().order_by("title")

    return render(request, "students/lecture_list.html", {"page_title": "Vorlesungen",
                                                          "lectures": lectures})

def delete_lecture(request, pk=None):
    if pk:
        lecture = Lecture.objects.get(pk=pk)
        lecture.delete()
        messages.success(request, "Lecture deleted")
    lectures = Lecture.objects.all().order_by("title")
    return render(request, "students/lecture_list.html", {"page_title": "Vorlesungen",
                                                          "lectures": lectures})

def lecture_details(request, pk=None):
    if pk:
        lecture = Lecture.objects.get(pk=pk)
    else:
        lecture = Lecture()

    if request.method == "POST":
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecture saved")
            return HttpResponseRedirect(reverse_lazy('lecture_list'))
        else:
            messages.error(request, "The form data is incorrect.")
    else:
        form = LectureForm(instance=lecture)

    return render(request, "students/lecture_details.html", {"page_title": "Add Lecture",
                                                             "form": form,
                                                             "lecture": lecture})

def student_details(request, pk=None):
    if pk:
        student = Student.objects.get(pk=pk)
    else:
        student = Student()

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student saved")
            return HttpResponseRedirect(reverse_lazy('student_list'))
        else:
            messages.error(request, "The form data is incorrect.")
    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_details.html", {"page_title": "Add Student",
                                                             "form": form})
