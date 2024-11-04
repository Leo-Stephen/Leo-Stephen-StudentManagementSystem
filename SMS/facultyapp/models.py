from django.apps import AppConfig

class FacultyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facultyapp'


from adminapp.models import StudentList
from django.db import models


class AddCourse(models.Model):
    COURSE_CHOICES = [
        ('AOOP', 'Advance Object-Oriented Programming'),
        ('PFSD', 'Python Full Stack Development'),
        ('DBMS', 'Database Management Systems'),
        ('DSA', 'Data Structures and Algorithms'),
        ('AI', 'Artificial Intelligence'),
    ]

    SECTION_CHOICES = [
        ('S1', 'Section S1'),
        ('S2', 'Section S2'),
        ('S3', 'Section S3'),
        ('S4', 'Section S4'),
        ('S5', 'Section S5'),
        ('S6', 'Section S6'),
        ('S7', 'Section S7'),
        ('S8', 'Section S8'),
        ('S9', 'Section S9'),
    ]

    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES)

    def __str__(self):
        return f'{self.student.Register_Number} - {self.course} ({self.section})'

class Marks(models.Model):
    COURSE_CHOICES = [
        ('AOOP', 'Advance Object-Oriented Programming'),
        ('PFSD', 'Python Full Stack Development'),
        ('DBMS', 'Database Management Systems'),
        ('DSA', 'Data Structures and Algorithms'),
        ('AI', 'Artificial Intelligence'),
    ]
    student = models.ForeignKey(StudentList, on_delete=models.CASCADE)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.Name} - {self.course}"
