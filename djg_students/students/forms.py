from django.forms import *
from students.models import *


class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ()
        labels = {"title": "Title",
                  "description": "Description"}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'enrolled_students' in self.fields:
            self.fields['enrolled_students'].required = False

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ()
        labels = {"lname": "Last name",
                  "fname": "First name",
                  "email": "E-Mail"}
