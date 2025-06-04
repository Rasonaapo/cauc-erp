from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
           
class TransactionCategory(models.Model):
    LEVEL_CHOICES = [
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
        ('4', 'Level 4'),
        ('5', 'Level 5'),
    ]
    type = models.CharField(max_length=50)
    detail = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='1')

    def __str__(self):
        return f"{self.type} - {self.detail}"
    
    class Meta:
        verbose_name_plural = 'Transaction Categories'


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('posted', 'Posted'),
        ('revoked', 'Revoked')
    ]

    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('TransactionCategory', on_delete=models.PROTECT, related_name='transactions')
    account = models.ForeignKey('finance.Account', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    status = models.CharField(max_length=50)
    reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
    cheque_number = models.CharField(max_length=50, null=True, blank=True)
    # created_by = models.CharField(max_length=50)
    bank = models.ForeignKey('payroll.Bank', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    payroll = models.ForeignKey('payroll.Payroll', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    loan = models.ForeignKey('payroll.Loan', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    financial_year = models.ForeignKey('finance.FinancialYear', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    supplier = models.ForeignKey('finance.Supplier', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    customer  = models.ForeignKey('finance.Student', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    employee = models.ForeignKey('hr.Employee', on_delete=models.PROTECT, related_name='transactions', null=True, blank=True)
    # For suppliers who have not been added to the system
    supplier_name = models.CharField(max_length=100, null=True, blank=True)
    # For customers who have not been added to the system
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    # For employees who have not been added to the system
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_description

    """ 
    create a method that will return the name of either the supplier from supplier field or purchase_order field
    it should return the name of the either the customer from customer field or sale field
    it should return the name of either the employee from employee field or employee_name field
    else it should return either supplier_name field or customer_name (whatever value is there)
    """   
    def get_client_name(self):
        if self.sale:
            return self.sale.customer
        elif self.purchase_order:
            return self.purchase_order.supplier
        elif self.employee:
            return self.employee
        elif self.customer:
            return self.customer
        elif self.supplier:
            return self.supplier
        elif self.customer_name:
            return self.customer_name
        elif self.supplier_name:
            return self.supplier_name
        elif self.employee_name:
            return self.employee_name
        
    def save(self, *args, **kwargs):
        from finance.models import FinancialYear
        # Ensure there is at least a financial year opened before committing any transaction
        if not FinancialYear.objects.filter(status='open').exists():
            raise ValidationError(_("There is no active financial year"))
        
        # Ensure the current open financial year is set
        if not self.financial_year:
            self.financial_year = FinancialYear.objects.get(status='open')
        
        # retrieve ledger records of transaction and ensure the sum of credit and debit is equal but convert negative amount into positive on the fly before computing
        if self.status == 'posted':
            credit = sum([ledger.amount for ledger in self.ledgers.filter(entry='credit')])
            debit = sum([ledger.amount for ledger in self.ledgers.filter(entry='debit')])  
            if credit < 0:
                credit = credit * -1
            if debit < 0:
                debit = debit * -1
            if credit != debit:
                raise ValidationError(_("Credit and Debit amount must be equal"))
            
        super().save(*args, **kwargs)


class Ledger(models.Model):
    ENTRY_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name="ledgers")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    account = models.ForeignKey('finance.Account', on_delete=models.PROTECT, related_name="account_ledgers")
    entry = models.CharField(max_length=10, choices=ENTRY_CHOICES)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.entry} {self.account} - {self.amount}"

    def save(self, *args, **kwargs):
        # Ensure double entry acconting principle
        if self.entry == 'credit':
            if self.account.account_category.category_type in ['asset', 'expense'] and self.amount > 0:
                raise ValidationError(_("Credit entry should be negative for asset and expense accounts"))  
            elif self.account.account_category.category_type in ['liability', 'equity', 'income'] and self.amount < 0:
                raise ValidationError(_("Credit entry should be positive for liability, equity and income accounts"))
        elif self.entry == 'debit':
            if self.account.account_category.category_type in ['asset', 'expense'] and self.amount < 0:
                raise ValidationError(_("Debit entry should be positive for asset and expense accounts"))  
            elif self.account.account_category.category_type in ['liability', 'equity', 'income'] and self.amount > 0:
                raise ValidationError(_("Debit entry should be negative for liability, equity and income accounts"))                
        
        super().save(*args, **kwargs)



