from django.urls import path
from . import views 
from django_filters.views import FilterView
from .filters import BudgetFilter


urlpatterns = [
    path('', views.index, name='index'),
    path('userdetails/', views.add_income_spending),
    path('display/', views.add_income_spending),
    path('display_income/', views.add_income_spending),
    path('history/', views.UserDetailsFilterView.as_view(), name='history'),   
    path('statistics/', views.statistics, name='statistics'),   
    path('pie_plot/', views.pie_plot, name='pie_plot'),
    path('line_plot/', views.line_plot, name='line_plot'), 
]


