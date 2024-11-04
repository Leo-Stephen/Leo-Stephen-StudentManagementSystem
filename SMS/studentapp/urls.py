from django.urls import path
from . import views

app_name = 'studentapp'  # Ensure you have this line

urlpatterns = [
    path('home/', views.StudentHomePage, name='StudentHomePage'),
    path('view_marks/', views.view_marks, name='view_marks'),
]