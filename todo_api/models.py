from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.


class GroupInfomation(models.Model):
    user_id = models.BigIntegerField()
    type = models.CharField(max_length=10)
    parent_id = models.BigIntegerField()
    combined_name = models.CharField(max_length=255)
    order_id = models.IntegerField()
    level = models.IntegerField()
    
    class Meta:
        db_table = 'groups'
    def __str__(self):
        return self.user_id

class TaskInfomation(models.Model):
    user_id = models.BigIntegerField()
    list_id = models.BigIntegerField()
    create_user_id = models.BigIntegerField()
    assigned_user_id = models.BigIntegerField()
    task_describe = models.TextField(max_length=5000)
    task_status = models.CharField(default='Not Complete', max_length=20)
    due_date = models.DateField()
    order_id = models.IntegerField()
    level = models.IntegerField()
    
    class Meta:
        db_table = 'tasks'
    def __str__(self):
        return self.user_id

class AssignInfomation(models.Model):
    user_id = models.BigIntegerField()
    list_id = models.BigIntegerField()
    join_user_id = models.BigIntegerField()

    class Meta:
        db_table = 'assigns'
    def __str__(self):
        return self.user_id