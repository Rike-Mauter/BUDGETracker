from .models import UserDetails
import django_filters

class BudgetFilter(django_filters.FilterSet):
    """
    Class used to filter the spendings database (UserDetails) by month and year
    """
    year_added = django_filters.NumberFilter(field_name='date_added', lookup_expr='year', label='Select Year   [yyyy]')
    month_added = django_filters.NumberFilter(field_name='date_added', lookup_expr='month', label='Select Month [mm]')
    
    class Meta:
        """
        This subclass defines the model to be filtered (UserDetails)
        """

        model = UserDetails
        fields = ['year_added', 'month_added']
        
