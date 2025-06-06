from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import Employee, Department, SMS, Designation, Skill, Job, JobHistory
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from datetime import date
from django.db.models import Q, Count
import json
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Employee
class EmployeeListApiView(LoginRequiredMixin, BaseDatatableView):
    model = Employee
    columns = ['id', 'first_name', 'last_name', 'employee_id', 'status', 'dob', 'phone_number', 'designation', 'hire_date', 'salary_grade', 'created_at']

    def render_column(self, row, column):

        if column == 'photo':
            return row.photo.url
        
        if column == 'employee_id':
            return row.employee_id
        
        if column == 'dob':
            return row.get_age()
        
        if column == 'designation':
            return row.designation.title if row.designation else '-'

        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')  # Format the created_at field

        if column == 'hire_date':
            return row.hire_date.strftime('%d %b, %Y')  # Format the created_at field

        if column == 'phone_number':
            return row.format_phone_number()  # Format the created_at field

        if column == 'salary_grade':
            return row.salary_grade.grade if row.salary_grade else '-'
        if column == 'status':
            status = 'success'
            if row.status == 'inactive':
                status = 'dark'
            elif row.status == 'on_leave':
                status = 'warning'
            elif row.status == 'terminated':
                status = 'danger label-table'
            elif row.status == 'probation':
                status = 'info'
            elif row.status == 'retired':
                status = 'primary'
            elif row.status == 'resigned':
                status = 'danger'

            return {'theme':status, 'status':row.get_status_display()}
            #  f"<span class='badge bg-{status}'>{row.get_status_display()}</span>"
        
        if column == 'first_name':  # Display employee photo with name
            photo_url = row.photo.url
            url = reverse('employee-detail', args=[row.id])

            # return f'<img src="{photo_url}"  alt="contact-img" title="contact-img" class="rounded-circle me-2 avatar-sm"> <a href="{url}" class="text-body fw-semibold">{row.first_name} {row.last_name}</a>'
        
            return {'photoURL':photo_url, 'staffURL':url, 'staffName':f"{row.first_name} {row.last_name}"}
        
        if column == 'id':
            return row.id
        
        return super().render_column(row, column)

    def get_initial_queryset(self):
        return Employee.objects.all()
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(department__department_name__icontains=search) |
                Q(salary_grade__grade__icontains=search)

            )
        # process filters from the template
        grade_id = self.request.GET.get('grade')
        bank_id = self.request.GET.get('bank')
        department_id = self.request.GET.get('department')
        designation_id = self.request.GET.get('designation')
        national_id = self.request.GET.get('id')
        status = self.request.GET.get('status')

        if grade_id:
            qs = qs.filter(salary_grade_id=grade_id)
        
        if status:
            qs = qs.filter(status=status)
        
        if bank_id:
            qs = qs.filter(bank_id=bank_id)
        
        if designation_id:
            qs = qs.filter(designation_id=designation_id)
        
        if national_id:
            qs = qs.filter(id_type_id=national_id)
        
        if department_id:
            qs = qs.filter(job__department_id=department_id)
        
        return qs
 
# Department

class DepartmentListApiView(LoginRequiredMixin, BaseDatatableView):
    model = Department
    columns = ['id', 'department_name', 'manager', 'location', 'employee_count', 'created_at']

    def render_column(self, row, column):
        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')  # Format the created_at field
        
        if column == 'manager':  # Display employee photo with name
            if row.manager is None:
                return 'N/A'
            else:
                photo_url = row.manager.photo.url
                return f'<img src="{photo_url}"  alt="contact-img" title="contact-img" class="rounded-circle me-2" heigth="20px" width="30px"> {row.manager.first_name} {row.manager.last_name}'
        
        if column == 'id':
            return row.id
        
        if column == 'employee_count':
            return row.employee_count or '-'
        
        return super().render_column(row, column)

    def get_initial_queryset(self):
        return Department.objects.annotate(employee_count=Count('jobs__employees'))
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(department_name__icontains=search) |
                Q(manager__last_name__icontains=search) |
                Q(manager__first_name__icontains=search) |
                Q(location__icontains=search)

            )
        return qs

class JobHistoryListApiView(LoginRequiredMixin, BaseDatatableView):
    model = JobHistory
    columns = ['id', 'employee', 'job_title', 'designation', 'start_date', 'end_date', 'created_at']

    def render_column(self, row, column):
        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')  # Format the date fields

        if column == 'start_date':
            return row.start_date.strftime('%d %b, %Y')  or '-'
        
        if column == 'end_date':
            if row.end_date:
                return row.end_date.strftime('%d %b, %Y') 
            else:
                return '-'

        if column == 'employee':  # Display employee photo with name
            url = reverse('employee-detail', args=[row.employee.id])

            return {'photoURL':row.employee.photo.url, 'staffURL':url,  'firstName':row.employee.first_name, 'lastName':row.employee.last_name }
            
        if column == 'id':
            return row.id
        
        if column == 'job_title':
            return row.job.job_title
        
        if column == 'designation':
            return row.designation.title
        
        return super().render_column(row, column)

    def get_initial_queryset(self):
        return JobHistory.objects.all()
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(job__job_title__icontains=search) |
                Q(designation__title__icontains=search) 
                # |
                # Q(location__icontains=search)
            )
        # get filters from drop downs
        job_id = self.request.GET.get('filterJob')
        designation_id = self.request.GET.get('filterDesignation')

        if job_id:
            qs = qs.filter(job_id=job_id)
        if designation_id:
            qs = qs.filter(designation_id=designation_id)
        return qs

class JobListApiView(LoginRequiredMixin, BaseDatatableView):
    model = Job
    columns = ['id',  'job_title', 'department', 'required_skills', 'min_salary', 'employee_count', 'created_at']

    def render_column(self, row, column):
        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')  # Format the date fields

        if column == 'required_skills':
            return row.display_required_skills()
        
        if column == 'department':
            return row.department.department_name

        if column == 'min_salary':
            return {'currency':row.get_currency_symbol(), 'minSalary':row.min_salary, 'maxSalary':row.max_salary }

        if column == 'employee_count':  # Display employee photo with name
            return row.employee_count
            
        if column == 'id':
            return row.id
        

        
        return super().render_column(row, column)

    def get_initial_queryset(self):
        return Job.objects.annotate(employee_count=Count('employees'))
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(employees__first_name__icontains=search) |
                Q(employees__last_name__icontains=search) |
                Q(job_title__icontains=search) |
                Q(department__department_name__icontains=search) |
                Q(required_skills__name__icontains=search)
                # |
                # Q(location__icontains=search)
            )
        # get filters from drop downs
        department_id = self.request.GET.get('filterDepartment')

        if department_id:
            qs = qs.filter(department_id=department_id)
        return qs
     
class DesignationListApiView(LoginRequiredMixin, BaseDatatableView):
    model = Designation
    columns = ['id', 'code', 'title', 'level', 'employee_count', 'created_at']

    def render_column(self, row, column):
        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')  # Format the created_at field
        
        if column == 'code':  # Display employee photo with name
            return 'N/A'if row.code is None else row.code

        if column == 'id':
            return row.id
        
        if column == 'employee_count':
            return row.employee_count or '-'
        
        return super().render_column(row, column)

    def get_initial_queryset(self):
        return Designation.objects.annotate(employee_count=Count('employees'))
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(code__icontains=search) |
                Q(title__icontains=search) |
                Q(level__icontains=search) 

            )

        # retrieve and process level filter
        level = self.request.GET.get('level')
        if level:
            qs = qs.filter(level=level)

        return qs


class SMSAPIView(LoginRequiredMixin, BaseDatatableView):
    model = SMS
    columns = ['id', 'message', 'sms_date', 'status', 'attendees', 'created_at']

    def render_column(self, row, column):
        if column == 'message':
            return row.message[:20] + '...' if len(row.message) > 20 else row.message 
        if column == 'sms_date':
            return row.sms_date.strftime('%d %b, %Y %I:%M %p')
        if column == 'created_at':
            return row.created_at.strftime('%d %b, %Y')
        if column == 'status':
            status = row.status
            theme = 'danger'
            if status == 'pending':
                theme = 'info'
            elif status == 'dispatched':
                theme = 'success'        
            return {'theme':theme, 'status':row.get_status_display()}

        if column == 'attendees':
            return len(row.get_sms_employees())

        return super().render_column(row, column)
    
    def get_initial_queryset(self):
        return SMS.objects.all()
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(message__icontains=search) |
                Q(status__icontains=search) 
            )
        return qs
    
def load_job_skills(request):
    job_id = request.GET.get('job_id')
    if job_id:
        job_skills = Skill.objects.filter(required_for_jobs__id=job_id).values('id', 'name')
        return JsonResponse(list(job_skills), safe=False)

    return JsonResponse([], safe=False)