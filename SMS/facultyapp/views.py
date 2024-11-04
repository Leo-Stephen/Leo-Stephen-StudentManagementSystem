from django.shortcuts import render, redirect
from .forms import AddCourseForm
from .models import AddCourse
from adminapp.models import StudentList
from django.core.mail import send_mail
from .forms import MarksForm
from django.conf import settings
from django.contrib.auth.models import User
from .models import StudentList

def FacultyHomePage(request):
    return render(request, 'facultyapp/FacultyHomePage.html')

def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            # Corrected the redirect URL format here
            return redirect('facultyapp:FacultyHomePage')  # Updated to use a colon (:)
    else:
        form = AddCourseForm()
    return render(request, 'facultyapp/add_course.html', {'form': form})  # Fixed typo in the template path

def view_student_list(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    student_courses = AddCourse.objects.all()
    if course:
        student_courses = student_courses.filter(course=course)
    if section:
        student_courses = student_courses.filter(section=section)
    students = StudentList.objects.filter(id__in=student_courses.values('student_id'))
    course_choices = AddCourse.COURSE_CHOICES
    section_choices = AddCourse.SECTION_CHOICES
    context = {
        'students': students,
        'course_choices': course_choices,
        'section_choices': section_choices,
        'selected_course': course,
        'selected_section': section,
    }
    return render(request, 'facultyapp/view_student_list.html', context)


from django.db import IntegrityError

def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            student = marks_instance.student
            course = marks_instance.course

            # Check for existing marks
            existing_marks = Marks.objects.filter(student=student, course=course).first()
            if existing_marks:
                # Update the marks if they already exist
                existing_marks.marks = marks_instance.marks
                existing_marks.save()
            else:
                # Save new marks if they don't exist
                marks_instance.save()

            # Send email notification
            student_user = student.user
            if student_user:  # Check if student_user exists
                user_email = student_user.email
                subject = 'Marks Entered'
                message = f'Hello, {student_user.first_name}, marks for {marks_instance.course} have been entered. Marks: {marks_instance.marks}'
                from_email = 'leo.stephen3737@gmail.com'
                recipient_list = [user_email]
                send_mail(subject, message, from_email, recipient_list)

            return render(request, 'facultyapp/marks_success.html')
    else:
        form = MarksForm()
    return render(request, 'facultyapp/post_marks.html', {'form': form})
