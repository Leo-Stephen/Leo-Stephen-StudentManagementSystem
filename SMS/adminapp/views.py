import random
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import render

def projecthomepage(request):
    return render(request, 'adminapp/ProjectHomepage.html')

def printpagecall(request):
    return render(request,'adminapp/printer.html')

def printpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'User input: {user_input}')
    a1 = {'user_input':user_input}
    return render(request,'adminapp/printer.html',a1)
def exceptionpagecall(request):
    return render(request,'adminapp/ExceptionExample.html')

def exceptpagecall(request):
    return render(request,'adminapp/UserRegister.html')

def exceptionpagelogic(request):
    if request.method=="POST":
        user_input=request.POST['user_input']
        result=None
        error_message=None
        try:
            num=int(user_input)
            result=10/num
        except Exception as e:
            error_message=str(e)
        return render(request,'adminapp/ExceptionExample.html',{'result':result,'error':error_message})
    return render(request,'adminapp/ExceptionExample.html')

def UserRegisterCall(request):
    return render(request,'adminapp/UserRegister.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegister.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/UserRegister.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'adminapp/ProjectHomepage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegister.html')
    else:
        return render(request, 'adminapp/UserRegister.html')

from  .forms import *

from django.shortcuts import render, redirect, get_object_or_404

def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLogin.html')

def UserLoginLogic(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pass = request.POST.get('user_pass')

        user = authenticate(request, username=user_id, password=user_pass)

        if user is not None:
            auth.login(request, user)
            if len(user_id) == 10:
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')
            elif len(user_id) == 4:
                return redirect('facultyapp:FacultyHomePage')
            else:
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/UserLogin.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/UserLogin.html')
    else:
        return render(request, 'adminapp/UserLogin.html')


def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request,'adminapp/add_task.html',{'form':form,'tasks':tasks})

def delete_task(request,pk):
    task = get_object_or_404(Task,pk=pk)
    task.delete()
    return redirect('add_task')

from .models import StudentList
from .forms import StudentForm

# def add_student(request):
#     if request.method=='POST':
#         form=StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = StudentForm()
#     return render(request,'adminapp/add_student.html',{'form':form})
from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})


def student_list(request):
    students = StudentList.objects.all()  # Fetch all students
    return render(request, 'adminapp/students_list.html', {'students': students})

import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render

def upload_sales(request):
    chart = None
    total_sales = None
    average_sales = None

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            # Read the CSV file, specifying the correct date format
            df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)

            # Ensure 'Sales' is numeric and handle errors
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

            # Drop rows with NaN values in 'Sales' or 'Date'
            df.dropna(subset=['Sales', 'Date'], inplace=True)

            total_sales = df['Sales'].sum()
            average_sales = df['Sales'].mean()

            # Extract month from the 'Date' column for grouping
            df['Month'] = df['Date'].dt.month
            monthly_sales = df.groupby('Month')['Sales'].sum()

            # Prepare month names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_sales.index = monthly_sales.index.map(lambda x: month_names[x - 1])

            # Create a pie chart with much larger size and better text properties
            plt.figure(figsize=(20, 20))  # Increased figure size for larger pie chart
            plt.pie(monthly_sales,
                    labels=monthly_sales.index,
                    autopct='%1.1f%%',
                    textprops={'fontsize': 24},  # Even larger font size for labels
                    labeldistance=1.25,  # Further distance for labels
                    pctdistance=0.85)    # Increased distance for percentage values
            plt.title('Sales Distribution per Month', fontsize=32)

            # Save the plot to a BytesIO object and encode it to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart = base64.b64encode(buffer.getvalue()).decode()
            plt.close()  # Close the plot to free memory
        except Exception as e:
            return render(request, 'adminapp/upload_sales.html', {
                'error': f"Error reading CSV: {str(e)}"
            })

    return render(request, 'adminapp/upload_sales.html', {
        'chart': chart,
        'total_sales': total_sales,
        'average_sales': average_sales,
    })



def datetimepagecall(request):
    return render(request, 'adminapp/datetimepage.html')

import datetime
import calendar
from datetime import timedelta

def datetimepagelogic(request):
    if request.method == "POST":
        number1 = int(request.POST['date1'])
        x = datetime.datetime.now()
        ran = x + timedelta(days=number1)
        ran1 = ran.year
        ran2 = calendar.isleap(ran1)
        if ran2 == False:
            ran3 = "Not leap year"
        else:
            ran3 = "Leap year"
    a1 = {'ran':ran, 'ran3':ran3, 'ran1':ran1, 'number1':number1}
    return render(request, 'adminapp/datetimepage.html', a1)


import random
import string
from django.shortcuts import render
from django.http import HttpResponse


# This function renders the page with the form
def randompagecall(request):
    return render(request, 'adminapp/randomExample.html')


# This function handles the logic of generating a random string
def randomlogic(request):
    ran = ""

    if request.method == 'POST':
        try:
            # Get the length for the random string from POST data, default to 10
            number1 = int(request.POST.get('number1', 10))

            # Generate a random alphanumeric string
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=number1))
        except ValueError:
            return HttpResponse("Invalid input. Please enter a valid integer.")

    context = {'ran': ran}
    return render(request, 'adminapp/randomExample.html', context)


from django.shortcuts import render

def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        try:
            # Get the input numbers and operation from the POST request
            num1 = float(request.POST.get('num1'))
            num2 = float(request.POST.get('num2'))
            operation = request.POST.get('operation')

            # Perform the requested operation
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2 if num2 != 0 else 'Infinity'
        except ValueError:
            result = "Invalid input. Please enter valid numbers."

    return render(request, 'adminapp/calculator.html', {'result': result})

from django.shortcuts import render

from .models import Feedback
def feedbackform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('textfield')

        # Save feedback to the database
        Feedback.objects.create(username=username, email=email, phone=phone, message=message)

        return render(request, 'adminapp/feedback_success.html')

    return render(request, 'adminapp/FeedbackForm.html')

