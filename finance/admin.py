from django.contrib import admin
from .models import *

# Operation models
@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'created_at', 'updated_at')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester', 'session', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'session', 'semester')

@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'period', 'status')
    list_filter = ('status', 'period')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'company_phone', 'current_balance', 'payment_terms', 'lead_time', 'city')
    search_fields = ('company_name', 'contact_person', 'city')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_years', 'number_of_credit', 'number_of_semester', 'department', 'session')
    list_filter = ('session', 'department')

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'program', 'level', 'status', 'email', 'phone_number', 'nationality', 'enrollment_date')
    list_filter = ('status', 'program', 'level', 'nationality')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'phone_number')

# Account models
@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_type', 'category_detail')
    list_filter = ('category_type',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'account_category', 'parent_account', 'balance', 'bank', 'active', 'is_system')
    list_filter = ('active', 'is_system', 'account_category', 'bank')
    search_fields = ('account_name', 'account_number')

# Transaction models
@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('type', 'detail', 'level')
    list_filter = ('type', 'level')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'category', 'account', 'status', 'reference', 'created_on')
    list_filter = ('status', 'category', 'account', 'date')
    search_fields = ('reference', 'description')

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'amount', 'account', 'entry', 'created_on')
    list_filter = ('entry', 'account')