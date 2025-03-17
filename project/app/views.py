from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, ReportForm
from .models import Record, Configuration
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import make_naive
from datetime import datetime


def authenticate_user(username, password):
    """
    Authenticate the user based on provided username and password.
    """
    return authenticate(username=username, password=password)


def handle_successful_login(request, username):
    """
    Handle actions after a successful login.
    """
    login(request, authenticate_user(username, request.POST['password']))
    return redirect('home')


def handle_failed_login(request):
    """
    Handle actions after a failed login attempt.
    """
    messages.error(request, "There was an error, Please try again")
    return redirect('home')


def home(request):
    """
    The home view handles both displaying the login form and processing
    login submissions.
    """
    key = '-created_at'
    users = User.objects.filter(is_staff=False)

    if request.user.is_authenticated:
        if request.user.is_staff:
            records = {}
            for user in users:
                record = Record.objects.filter(user=user).order_by(key).first()
                records[user] = record.created_at if record else ''
        else:
            records_l = Record.objects.filter(user=request.user).order_by(key)
            paginator = Paginator(records_l, 10)  # Show 10 records per page
            page_number = request.GET.get('page')
            records = paginator.get_page(page_number)
    else:
        records = []

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate_user(username, password)

        if user:
            return handle_successful_login(request, username)
        else:
            return handle_failed_login(request)

    return render(request, 'home.html', {'records': records})


def logout_user(request):
    """
    Log out the user and redirect to home page.
    """
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')


def register_user(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            authenticate(username=username, password=password)
            messages.success(request,
                             f"You have successfully registered {username}!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def add_record(request):
    """
    Handle adding a new record.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user
                record.save()
                messages.success(request, "Record added successfully!")
                return redirect('home')
        else:
            form = AddRecordForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add a record!")
        return redirect('home')


def output_record(request, id):
    """
    Handle output an existing record.
    """
    if request.user.is_authenticated:
        current_record = get_object_or_404(Record, id=id)
        if request.method == "POST":
            form = ReportForm(request.POST, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been updated!")
                return redirect('home')
        else:
            form = ReportForm(instance=current_record)
        return render(request, 'report_record.html', {'form': form, 'id': id})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')


def customer_record(request, id):
    """
    View a specific record.
    """
    print("customer_record")
    print(id)
    if request.user.is_authenticated:
        customer_record = get_object_or_404(Record, id=id)
        return render(request, 'record.html',
                      {'customer_record': customer_record,
                       'id': id})
    else:
        messages.success(request, "You must be logged in to view a record!")
        return redirect('home')


def delete_record(request, id):
    """
    Handle deleting a record.
    """
    if request.user.is_authenticated and request.user.is_staff:
        delete_it = get_object_or_404(Record, id=id)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be staff to delete a record!")
        return redirect('home')


def update_record(request, id):
    """
    Handle updating a record.
    """
    if request.user.is_authenticated:
        current_record = get_object_or_404(Record, id=id)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')


@login_required
def user_records(request, id):
    """
    View to show all records from a specific user.
    """
    user = get_object_or_404(User, id=id)
    records = Record.objects.filter(user=user).order_by('-created_at')
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)
    return render(request, 'user_records.html', {'user_name': user,
                                                 'records': records})


def report(request):
    """
    Generate an Excel report with all the information from the database.
    """
    configuration = Configuration.objects.all().values().first()
    file_name = configuration['file_name']
    users = configuration['users']
    # email = configuration['email']

    if configuration['users'] == 'all':
        records = Record.objects.all().values()
    else:
        records = Record.objects.filter(user=users).values()

    records_list = list(records)

    for record in records_list:
        for key, value in record.items():
            if isinstance(value, datetime):
                record[key] = make_naive(value)

    df = pd.DataFrame(records_list)

    type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=type)
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Records')

    return response


@login_required
def configure_excel(request):
    """
    Configure the Excel report settings.
    """
    users = User.objects.filter(is_staff=False)
    if request.method == 'POST':
        file_name = request.POST['fileName']
        record_type = request.POST['recordType']
        email = request.POST['email']

        configuration, created = Configuration.objects.update_or_create(
            defaults={'file_name': file_name,
                      'email': email,
                      'users': record_type})

        return redirect('home')
    file_name = 'report'
    return render(request, 'configure_excel.html', {'users': users,
                                                    'name': file_name})
