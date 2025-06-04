from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(SalaryGrade) 
class SalaryGradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'step', 'amount', )

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'active', )

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('year', 'block', 'rate', )

@admin.register(SalaryStep)
class SalaryStepAdmin(admin.ModelAdmin):
    list_display = ['step']



@admin.register(SalaryItem)
class SalaryItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'alias_name', 'effect', 'rate_type', 'rate_amount', 'rate_dependency', 'expires_on', 'staff_source', )

@admin.register(StaffSalaryItem)
class StaffSalaryItemAdmin(admin.ModelAdmin):
    list_display = ('salary_item', 'employee', 'variable', 'amount', 'active', )

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'loan_type', 'principal_amount', 'interest_rate', 'monthly_installment', 'duration_in_months', 'total_repayable_amount', 'outstanding_balance', 'status', 'applied_on', 'approved_on', 'active_on', 'deduction_end_date', )
    list_filter = ('loan_type', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount_paid', 'date_paid', 'payment_reference', )

@admin.register(CreditUnion)
class CreditUnionAdmin(admin.ModelAdmin):
    list_display = ('union_name', 'amount',  'deduction_start_date', 'deduction_end_date', )

@admin.register(StaffCreditUnion)
class StaffCreditUnionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'credit_union', 'amount', 'deduction_start_date', 'deduction_end_date')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('process_month', 'process_year', 'description',  'posted',  'payment_rate' )

@admin.register(StaffCreditUnionDeduction)
class StaffCreditUnionDeductionAdmin(admin.ModelAdmin):
    list_display = ('staff_credit_union', 'amount_paid', 'date_paid', )

@admin.register(PayrollError)
class PayrollErrorAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'employee',  'error_category', 'error_details', 'resolved', )
    list_filter = ['error_category']

@admin.register(PayrollItem)
class PayrollItemAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'employee', 'item_type', 'dependency', 'amount', 'description', 'entry', 'credit_union', 'bank', 'salary_item', 'loan', )