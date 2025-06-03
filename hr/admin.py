from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'status',  'photo', 'email', 'phone_number', 'hire_date', 'salary_grade', 'job', 'ssnit', 'tin', 'bank', 'branch', 'account_number', 'id_type', 'id_number','display_employee_skill')
    list_filter = ['skills']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'manager', 'location', )

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'min_salary', 'max_salary', )

@admin.register(JobHistory)
class JobHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'job',  'designation')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'document_file')

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'allow_multiple', )

@admin.register(NationalIDType)
class NationalIDTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('message', 'sms_date', 'display_sms_job', 'display_sms_department', 'display_sms_grade', 'created_at', 'updated_at', 'status', )

@admin.register(Guarantor)
class GuarantorAdmin(admin.ModelAdmin):
    list_display = ('employee', 'guarantor_name', 'guarantor_phone_number', )

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'level', )


# Leave
@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'entitlement', 'method', 'allow_rollover' )

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'accrued_days', 'used_days', )

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'days_requested', )

@admin.register(PublicHoliday)
class PublicHolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ['date']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ['category']

   