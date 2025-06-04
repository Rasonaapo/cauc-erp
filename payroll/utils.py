from hr.models import  Employee
from .models import SalaryItem
from datetime import datetime


def item_expiry_status(expiry_date):
   today = datetime.now().date()
   return today < expiry_date

def compute_factor(employee, rate_amount, rate_dependency):
    basic_salary = employee.salary_grade.amount

    # if rate dependency is Basic, use rate amount to get the percentage of that..
    if rate_dependency == 'Basic':
        amount = (rate_amount / 100) * basic_salary
    else:
        # get the rate amount of the selected item whose id is rate dependency
        salary_item = SalaryItem.objects.get(id=rate_dependency)
        amount = (rate_amount / 100) * salary_item.rate_amount
    
    return amount

# a method to synthetically retrieve eligible employees for credit union to make update seamless with transactions
def get_filtered_staff_credit_union(all_employee, department, applicable_to, excluded_from):

    eligible_employee = Employee.objects.active()

    # if all employee is checked, return all
    if all_employee:
        return eligible_employee
    
    # Navigate through the filters if not all employee was specified
    if department.exists():
        eligible_employee = eligible_employee.filter(job__department__in=department.all())
    if applicable_to.exists():
        eligible_employee = applicable_to.all()
    if excluded_from.exists():
        eligible_employee = eligible_employee.exclude(id__in=excluded_from.values_list('id', flat=True))

    return eligible_employee

def get_filtered_staff_payroll(data):
    eligible_employee = Employee.objects.active()

    if data['employment_type'].exists():
        eligible_employee = eligible_employee.filter(employment_type__in=data['employment_type'].all())
    
    if data['step'].exists():
        eligible_employee = eligible_employee.filter(salary_grade__grade_step__in=data['step'].all())

    if data['salary_grade'].exists():
        eligible_employee = eligible_employee.filter(salary_grade__in=data['salary_grade'].all())
    
    if data['designation'].exists():
        eligible_employee = eligible_employee.filter(designation__in=data['designation'].all())

    if data['department'].exists():
        eligible_employee = eligible_employee.filter(job__department__in=data['department'].all())
    
    if data['applicable_to'].exists():
        eligible_employee = eligible_employee.filter(id__in=data['applicable_to'].values_list('id', flat=True))
    
    if data['excluded_from'].exists():
        eligible_employee = eligible_employee.exclude(id__in=data['excluded_from'].values_list('id', flat=True))

    return eligible_employee

    

