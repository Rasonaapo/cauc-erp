from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

class Year(models.Model):
    year = models.IntegerField(verbose_name='Year', unique=True, help_text="e.g. 2023/2024")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.year)


class AcademicYear(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]
    SEMESTER_CHOICES = [('1', 'First Semester'), ('2', 'Second Semester'), ('all', 'All Semesters')]
    SESSION_CHOICES = [('regular', 'Regular'), ('sandwich', 'Sandwich'), ('distance', 'Distance Learning')]
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1')
    year = models.ForeignKey('Year', on_delete=models.CASCADE, related_name='academic_years', verbose_name='Academic Year')
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default='regular')

    def __str__(self):
        return f"{self.year_name} {self.semester} ({self.get_status_display()})"

    class Meta:
        unique_together = ('start_date', 'end_date', 'session')

    def clean(self):
        # Ensure end date is greater than start date
        if self.start_date > self.end_date:
            raise ValidationError(_("End date must be greater than start date"))
    
    # Ensure that there is no overlapping academic year using the start, end date and session
        if AcademicYear.objects.filter(
            start_date__lte=self.start_date, 
            end_date__gte=self.start_date,
            session=self.session
        ).exists():
            raise ValidationError(_("Overlapping academic year for the same session"))
    
    # Ensure that only one academic year with session is open at a time
        if self.status == 'open':
            if AcademicYear.objects.filter(status='open', session=self.session).exclude(id=self.id).exists():
                raise ValidationError(_("Only one academic year can be open at a time for the same session"))

class FinancialYear(models.Model):
    PERIOD_CHOICES = [('3', '3 Months'), ('6', '6 Months'), ('9', '9 Months'), ('12', '12 Months')]
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed')]
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='12')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"{self.start_date} to {self.end_date} ({self.get_status_display()})"
    
    def clean(self):
        # Ensure end date is greater than start date
        if self.start_date > self.end_date:
            raise ValidationError(_("End date must be greater than start date"))
        
        # Ensure there is no overlapping financial year
        if FinancialYear.objects.filter(start_date__lte=self.start_date, end_date__gte=self.start_date).exists():
            raise ValidationError(_("Overlapping financial year"))
        
        # Ensure when period is chosen, the start and end date range conform to the peroid, eg 3 months period should have a range of 3 months
        if self.period:
            period = int(self.period)
            period_in_weeks = period * 4
            if self.end_date - self.start_date != timedelta(weeks=period_in_weeks):
                raise ValidationError(_(f"{period} months period should have a range of {period} months"))

        # Ensure only one financial year is open at a time
        if self.status == 'open':
            if FinancialYear.objects.filter(status='open').exclude(id=self.id).exists():
                raise ValidationError(_("Only one financial year can be open at a time"))
 
 
class Supplier(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Company Name", unique=True)
    tax_number = models.CharField(max_length=50, verbose_name="Tax Identification Number", null=True, blank=True)   
    contact_person = models.CharField(max_length=255, verbose_name="Contact Person")
    contact_position = models.CharField(max_length=100, null=True, blank=True, verbose_name="Position")
    contact_phone = models.PositiveIntegerField(verbose_name="Phone Number" )
    contact_email = models.EmailField(null=True, blank=True, verbose_name="Email Address")
    company_phone = models.CharField(max_length=20, verbose_name="Company Phone")
    company_email = models.EmailField(verbose_name="Company Email")
    website = models.URLField(null=True, blank=True)
    address = models.TextField(help_text="Digital address of the supplier or Post Address")
    city = models.CharField(max_length=100, verbose_name="City", null=True)
    
    # Supply Details
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.PositiveIntegerField(default=30, help_text="Payment terms in days")
    lead_time = models.PositiveIntegerField(help_text="Average lead time in days")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['contact_person']),
        ]

    def clean(self):
        if self.current_balance < 0:
            raise ValidationError(_("Supplier balance cannot be negative"))
        
        if self.payment_terms <= 0:
            raise ValidationError(_("Payment terms must be a positive number"))
    
    def __str__(self):
        return self.company_name.capitalize()

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="ISO Alpha-3 code, e.g. 'GHA' for Ghana")

    def __str__(self):
        return self.name

class Program(models.Model):
    SESSION_CHOICES = [
        ('regular', 'Regular'),
        ('evening', 'Evening'),
        ('weekend', 'Weekend'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.PositiveIntegerField(default=4)
    number_of_credit = models.PositiveIntegerField(default=15, verbose_name="Mininum Credit Hours", help_text="Total number of credits required to complete the program")
    number_of_semester = models.PositiveIntegerField(default=8, verbose_name="Number of Semesters", help_text="Total number of semesters required to complete the program")
    department = models.ForeignKey('hr.Department', null=True, blank=True, on_delete=models.CASCADE, related_name='programs', verbose_name="Department")
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default='regular')
    
    def __str__(self):
        return f"{self.name.capitalize()} ({self.code})"
    
    # create a method that will make self.code into upper case upon save
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(Program, self).save(*args, **kwargs)

class Level(models.Model):
    name = models.CharField(max_length=20)  # e.g., "100", "200", "300"
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    STUDENT_STATUS = [
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
    ]

    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    other_names = models.CharField(max_length=100, blank=True, null=True, verbose_name="Other Names")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="Phone Number")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    guardian_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Guardian Name")
    guardian_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Guardian Phone")
    guardian_email = models.EmailField(null=True, blank=True, verbose_name="Guardian Email")
    nationality = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now, verbose_name="Enrollment Date")
    status = models.CharField(max_length=20, choices=STUDENT_STATUS, default='active')
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"


