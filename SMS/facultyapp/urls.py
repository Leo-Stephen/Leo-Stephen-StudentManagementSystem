from django.urls import path
from . import views

app_name = 'facultyapp'

urlpatterns = [
    path('home/', views.FacultyHomePage, name='FacultyHomePage'),
    path('add_course/',views.add_course, name='add_course'),
    path('view_student_list/',views.view_student_list, name='view_student_list'),
    path('post_marks/', views.post_marks, name='post_marks'),
]