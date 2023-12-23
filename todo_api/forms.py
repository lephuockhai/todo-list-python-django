# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import models

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {'email': 'Email'}

class TaskChangeForm(forms.ModelForm):
    task_status = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    list_id = forms.IntegerField(required=False)  # Hoặc True nếu bạn muốn yêu cầu giá trị này
    due_date = forms.DateField(required=False)
    class Meta:
        model= models.TaskInfomation
        fields= ['task_describe', 'task_status', 'due_date', 'list_id']
        
class ListGroupChangeForm(forms.ModelForm):
    parent_id = forms.IntegerField(required=False)
    class Meta:
        model= models.GroupInfomation
        fields= ['combined_name', 'parent_id']

class AssignsForm(forms.ModelForm):
    email = forms.EmailField(label='User Email')
    # user_id = forms.IntegerField(required=True)
    list_id = forms.IntegerField(required=True)
    # join_user_id = forms.IntegerField(required=True)
    class Meta:
        model= models.AssignInfomation
        fields= ['list_id']

class AssignForTaskForm(forms.ModelForm):
    assigned_user_id= forms.IntegerField(required=True)
    class Meta:
        model= models.TaskInfomation
        fields= ['assigned_user_id']

class AssignUserForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())
    user_email = forms.EmailField(label='User Email')
    