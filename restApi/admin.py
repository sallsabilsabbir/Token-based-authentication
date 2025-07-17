from django.contrib import admin
from . models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','emp_id','emp_name','emp_department','emp_salary','emp_Contact','emp_address']


