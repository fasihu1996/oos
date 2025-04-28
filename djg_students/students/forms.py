from django.forms import *
from students.models import *


class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ()
        labels = {"title": "Title",
                  "description": "Description"}

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ()
        labels = {"lname": "Last name",
                  "fname": "First name",
                  "email": "E-Mail"}
