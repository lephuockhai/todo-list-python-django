# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import GroupInfomation, TaskInfomation, AssignInfomation
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInfomation
        fields = ["user_id", "list_id", "task_id", "create_user_id", "assigned_user_id", "task_describe", "task_status", "due_date", "order_id", "level"]

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfomation
#         fields = ["user_id", "username", "password", "email"]
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInfomation
        fields = ["user_id", "combined_id", "type", "parent_id", "combined_name", "order_id", "level"]
    
class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignInfomation
        fields = ["user_id", "list_id", "join_user_id"]
    