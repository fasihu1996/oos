from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
import json
import tempfile
import subprocess
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
import os

from students.forms import *
from students.models import *

def typst_escape(text):
    # Escape backslashes and double quotes for Typst
    return str(text).replace("\\", "\\\\").replace('"', '\\"')

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

def generate_lecture_pdf(request, pk):
    # Get lecture and enrolled students
    lecture = get_object_or_404(Lecture, pk=pk)
    students = Student.objects.filter(lectures=lecture) if hasattr(Student, 'lectures') else []

    # Build Typst data structure as valid Typst code (use parentheses for Typst objects)
    students_typst = ",\n    ".join(
        f'(lname: "{typst_escape(s.lname)}", fname: "{typst_escape(s.fname)}", email: "{typst_escape(s.email)}")'
        for s in students
    )
    typst_data = f'(\n  title: "{typst_escape(lecture.title)}",\n  description: "{typst_escape(lecture.description)}",\n  student_count: {len(students)},\n  students: [\n    {students_typst}\n  ]\n)'

    # Read Typst template from file
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'typst', 'lecture_report.typ')
    with open(template_path, encoding='utf-8') as f:
        typst_template = f.read()

    # Insert typst_data into template
    typst_content = typst_template.format(typst_data=typst_data)

    # Write Typst content to a temp file (ensure UTF-8 encoding)
    with tempfile.NamedTemporaryFile(suffix='.typ', mode='w', encoding='utf-8', delete=False) as typ_file:
        typ_file.write(typst_content)
        typ_file_path = typ_file.name

    # Print Typst content for debugging
    print("Generated Typst content:\n", typst_content)

    # Prepare output PDF file
    pdf_file_handle, pdf_file_path = tempfile.mkstemp(suffix='.pdf')
    os.close(pdf_file_handle)

    try:
        result = subprocess.run(
            ['typst', 'compile', typ_file_path, pdf_file_path],
            check=True,
            capture_output=True,
            text=True
        )
        print('Typst stdout:', result.stdout)
        print('Typst stderr:', result.stderr)
        os.unlink(typ_file_path)
        pdf_file = open(pdf_file_path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{lecture.title}_report.pdf"'
        # Clean up after response is closed
        def cleanup_file(file_obj, file_path):
            file_obj.close()
            if os.path.exists(file_path):
                os.unlink(file_path)
        import functools
        response.close = functools.partial(cleanup_file, pdf_file, pdf_file_path)
        return response
    except subprocess.CalledProcessError as e:
        print('Typst error output:', e.stderr)
        if os.path.exists(typ_file_path):
            os.unlink(typ_file_path)
        if os.path.exists(pdf_file_path):
            os.unlink(pdf_file_path)
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)