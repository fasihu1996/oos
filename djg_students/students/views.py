from django.contrib import messages
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime
import subprocess
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
    
    enrolled_students = lecture.enrolled_students.all() if lecture.pk else []

    return render(request, "students/lecture_details.html", {"page_title": "Add Lecture",
                                                             "form": form,
                                                             "lecture": lecture,
                                                             "enrolled_students": enrolled_students})

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
    """
    Generate a PDF report for a lecture using Typst and return it as a download.
    """
    lecture = get_object_or_404(Lecture, pk=pk)
    students = lecture.enrolled_students.all()
    
    downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Generate filenames with timestamp to avoid overwrites
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    typ_fp = os.path.join(downloads_dir, f'lecture_{lecture.pk}_{timestamp}.typ')
    pdf_fp = os.path.join(downloads_dir, f'lecture_{lecture.pk}_{timestamp}.pdf')
    
    # Create a complete table in Typst syntax
    if students:
        rows = ['[*Last Name*], [*First Name*]']
        for s in students:
            row = f'[{typst_escape(s.lname)}], [{typst_escape(s.fname)}]'
            rows.append(row)
        
        rows_code = ",\n      ".join(rows)
        
        table_typst = f'table(\n    columns: (1fr, 1fr),\n    inset: 8pt,\n    {rows_code}\n  )'
    else:
        table_typst = '[No students are currently enrolled in this lecture.]'

    typst_data = (
        f'(\n  title: "{typst_escape(lecture.title)}",\n'
        f'  description: "{typst_escape(lecture.description)}",\n'
        f'  student_count: {len(students)},\n'
        f'  table_rows: {table_typst}\n)'
    )

    template_path = os.path.join(
        os.path.dirname(__file__), '..', 'templates', 'typst', 'lecture_report.typ'
    )
    with open(template_path, encoding='utf-8') as f:
        typst_template = f.read()

    typst_content = typst_template.format(typst_data=typst_data)

    with open(typ_fp, 'w', encoding='utf-8') as f:
        f.write(typst_content)
    
    try:
        subprocess.run(
            ['typst', 'compile', typ_fp, pdf_fp],
            check=True,
            capture_output=True,
            text=True
        )
        # Serve the PDF
        pdf_file = open(pdf_fp, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{lecture.title}_report.pdf"'
        
        return response
    except subprocess.CalledProcessError as e:
        print('Typst error output:', e.stderr)
        if os.path.exists(typ_fp):
            os.unlink(typ_fp)
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)