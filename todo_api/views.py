from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from . import forms
from . import models

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid(): # form valid
            user = form.save()
            return redirect('login')  # move to Login page after finish Register .../login/
        else:
            messages.error(request, form.errors) # form invalid
    else:
        form = forms.RegisterForm()
    return render(request, 'register.html', {'form': form})

@permission_classes([AllowAny])
def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                # Trả về JSON nếu là API request
                response_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'token': access_token,
                                    }

                # Điều hướng nếu là request thông thường
                return render(request, 'home.html', {'user_data': response_data})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            print("errors: ",form.errors)
    # Trả về trang đăng nhập nếu không phải là yêu cầu POST
    return render(request, 'login.html', {'form': AuthenticationForm()})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form':form})

@login_required
@csrf_protect
def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            user_info = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                }
            return render(request, 'view_profile.html', {'user_info': user_info})
    return render(request, 'view_profile.html')
        
def change_profile(request):
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = forms.UserProfileForm(instance = request.user)
    return render(request, 'change_profile.html', {'form':form})

@csrf_exempt
def createtask(request):
    tasks = models.TaskInfomation.objects.filter(user_id=request.user.id)
    lists = models.GroupInfomation.objects.filter(user_id=request.user.id, type='list')
    if request.method == 'POST':
        form = forms.TaskChangeForm(request.POST)
        current_user = request.user
        if form.is_valid():
            list_id = form.cleaned_data.get('list_id', None)
            assigned_user_id = form.cleaned_data.get('assigned_user_id', None)
            task_describe = form.cleaned_data['task_describe']
            task_status = form.cleaned_data['task_status']
            due_date = form.cleaned_data.get('due_date', None)
            order_id = models.TaskInfomation.objects.count() + 1

            print("list_id:", list_id, "due_date: ", due_date)  # In giá trị để kiểm tra
 
            new_task = models.TaskInfomation.objects.create(
                user_id=current_user.id,
                list_id=list_id,
                create_user_id=current_user.id,
                assigned_user_id=assigned_user_id,
                task_describe=task_describe,
                task_status = 'Complete' if task_status else 'Not Complete',
                due_date=due_date,
                order_id=order_id,
                level=1 if list_id is None else 2,  # Giá trị mặc định cho level,
            )
            tasks = models.TaskInfomation.objects.filter(user_id=request.user.id, level=1)
            lists = models.GroupInfomation.objects.filter(user_id=request.user.id, type='list')
            return render(request,'create_task.html', {'tasks': tasks, 'lists': lists, 'new_task': new_task})
        else:
            print(form.errors)
    return render(request, 'create_task.html', {'tasks': tasks, 'lists': lists})

@csrf_exempt
def createlist(request):
    lists = models.GroupInfomation.objects.filter(user_id = request.user.id, type= 'list')
    groups = models.GroupInfomation.objects.filter(user_id = request.user.id, type='group')

    if request.method == 'POST':
        form = forms.ListGroupChangeForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data.get('parent_id', None)
            print(parent_id)
            combined_name = form.cleaned_data.get('combined_name')
            order_id = models.GroupInfomation.objects.count() + 1
            
            newlist = models.GroupInfomation.objects.create(
                user_id = request.user.id,
                type = 'list',
                parent_id = parent_id,
                combined_name = combined_name,
                order_id= order_id,
                level = 1 if parent_id is None else 2,
            )
            lists = models.GroupInfomation.objects.filter(user_id = request.user.id, type= 'list')
            groups = models.GroupInfomation.objects.filter(user_id = request.user.id, type='group')
            return render(request, 'create_list.html', {'lists':lists, 'groups':groups, 'new_list': newlist})
        else:
            messages.error(request, form.errors)
    return render(request, 'create_list.html', {'lists': lists, 'groups': groups})

@csrf_exempt
def creategroup(request):
    groups = models.GroupInfomation.objects.filter(user_id = request.user.id, type='group')
    if request.method == 'POST':
        form = forms.ListGroupChangeForm(request.POST)
        if form.is_valid():
            current_user = request.user
            combined_name = form.cleaned_data.get('combined_name')
            order_id = models.GroupInfomation.objects.count() + 1
            
            new_group = models.GroupInfomation.objects.create(
                user_id = current_user.id,
                type = 'group',
                parent_id = None,
                combined_name = combined_name,
                order_id= order_id,
                level = 1,
            )
            groups = models.GroupInfomation.objects.filter(user_id = request.user.id, type='group')
            return render(request, 'create_group.html', {'groups':groups, 'new_group': new_group})
        else:
            messages.error(request, form.errors)
    return render(request, 'create_group.html', {'groups': groups})

@login_required
def home(request):
    return render(request, 'home.html')

def log_out(request):
    logout(request)
    return redirect('login')  # Chuyển hướng sau khi đăng xuất

@csrf_exempt
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = models.TaskInfomation.objects.get(id=task_id)
        task.task_status = 'Complete' if task.task_status == 'Not Complete' else 'Not Complete'
        task.save()
    return redirect('createtask')

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'POST':
        task = models.TaskInfomation.objects.get(id=task_id)
        task.delete()
    return redirect('createtask')

@csrf_exempt
def delete_list(request, list_id):
    if request.method == 'POST':
        list = models.GroupInfomation.objects.get(id=list_id)
        list.delete()
    return redirect('createlist')

@csrf_exempt
def delete_group(request, group_id):
    if request.method == 'POST':
        group = models.GroupInfomation.objects.get(id=group_id)
        group.delete()
    return redirect('creategroup')

def assigns_to_list(request):
    lists = models.GroupInfomation.objects.filter(user_id=request.user.id, type='list')
    if request.method == 'POST':
        form = forms.AssignsForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            list_id = form.cleaned_data.get('list_id')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Email is not registered.')
                return render(request, 'assigns.html', {'form': form})
            
            new_assign = models.AssignInfomation.objects.create(
                user_id= request.user.id,
                list_id= list_id,
                join_user_id= user.id,
            )
            return render(request, 'assigns.html', {'form': form, 'lists': lists})
        else:
            print(form.errors)
    else:
        form = forms.AssignsForm(request.user)
    return render(request, 'assigns.html', {'form': form, 'lists': lists})

def assigns_to_task(request, list_id):
    try:
        list_data = models.GroupInfomation.objects.get(id= list_id, type= 'list', user_id= request.user.id)
    except models.GroupInfomation.DoesNotExist:
        messages.error(request, 'List not found.')
        return redirect('your_redirect_view_name')
    
    tasks = models.TaskInformation.objects.filter(list_id=list_data.id)
    form = form.AssignUserForm()

    if request.method == 'POST':
        form = forms.AssignUserForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            user_email = form.cleaned_data['user_email']
            try:
                user = User.objects.get(email=user_email)
                models.AssignInfomation.objects.create(user_id=request.user.id, task_id=task_id, join_user_id=user.id)
                messages.success(request, f'User {user.email} assigned to the task successfully.')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
        else:
            messages.error(request, 'Invalid form submission.')
    return render(request, 'task_list.html', {'your_list': list_data, 'tasks': tasks, 'form': form})