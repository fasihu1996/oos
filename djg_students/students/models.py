from django.db import models


# Create your models here.

class Student(models.Model):
    lname = models.CharField(max_length=30)
    fname = models.CharField(max_length=30)
    email = models.EmailField(blank=False)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Lecture(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    enrolled_students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.title}"

