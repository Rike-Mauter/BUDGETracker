from django import forms
from datetime import date
from django.forms import ModelForm
from .models import UserDetails
from .models import UserIncome


class UserModelForm(ModelForm):
    """
    Class that allows the user to add new spending information to the database. 
    """
    current_date = date.today()
    YEARS = [x for x in range(current_date.year - 1, current_date.year + 6)]
    today = current_date.strftime("%Y-%m-%d")

    date_added = forms.DateField(initial=today, widget=forms.SelectDateWidget(years=YEARS))
 
    class Meta:
        """
        The subclass defines, to which model the form refers to.
        """
        model = UserDetails
        fields = ['expense_name', 'cost', 'date_added', 'category', 'notes']


class AddIncome(ModelForm):
    """
    Class that allows the user to add new income information to the database. 
    """
    current_date = date.today()
    YEARS = [x for x in range(current_date.year - 1, current_date.year + 6)]
    today = current_date.strftime("%Y-%m-%d")

    date_added = forms.DateField(initial=today, widget=forms.SelectDateWidget(years=YEARS))
 
    class Meta:
        """
        The subclass defines, to which model the form refers to.
        """
        model = UserIncome
        fields = ['income_name', 'income', 'date_added']


       