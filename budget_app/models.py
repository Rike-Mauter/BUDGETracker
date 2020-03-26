
from django.db import models
from django.contrib.auth.models import User 


CHOICES = (
    ('rent', 'Rent'),  
    ('grocery', 'Grocery'), 
    ('shopping', 'Shopping'), 
    ('gym', 'Gym'), 
    ('phone', 'Phone'), 
    ('freetime', 'Freetime'), 
    ('other', 'Other')
)

class UserDetails(models.Model):
    """
    This model class defines a spending.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="new_spending", null=True)  
    expense_name = models.CharField(max_length=255)
    cost = models.FloatField()
    date_added = models.DateTimeField()
    category = models.CharField(max_length=25, choices=CHOICES)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __repr__(self): 
        return f'UserDetails(models.Model)'

    def __str__(self):
        return self.expense_name


class UserIncome(models.Model):
    """
    This model class defines an income.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="new_income", null=True)
    income_name = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    income = models.FloatField()

    def __repr__(self): 
        return f'UserIncome(models.Model)'

    def __str__(self): 
        return self.income_name





