from django.shortcuts import render   
from django.http import HttpResponse
from datetime import date
import calendar
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from .models import UserDetails
from .models import UserIncome
from .forms import UserModelForm
from .forms import AddIncome
from .filters import BudgetFilter
from django.db.models import Sum 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


@login_required
def index(request, year=date.today().year, month=date.today().month):
    
    """

    Function based view for the index.html that shows the current date in the title 
    and sums up the income, spendings and the left budget.

    """

    year = int(year) 
    month = int(month)
    month_name = calendar.month_name[month]
    title = "This is your current budget - %s %s" % (month_name, year)

    total_budget = UserIncome.objects.filter(user=request.user, date_added__year=year, date_added__month=month).aggregate(budget=Sum('income')) 
    if total_budget['budget'] == None: 
        total_budget['budget'] = 0

    total_expenses = UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month).aggregate(expenses=Sum('cost')) 
    if total_expenses['expenses'] == None: 
        total_expenses['expenses'] = 0

    left_budget = total_budget['budget']-total_expenses['expenses']

    return render(request, 'budget_app/index.html', {'title': title, 'total_budget': total_budget['budget'] or 0, 'total_expenses': total_expenses['expenses'] or 0, 'left_budget': left_budget})


def add_income_spending(request):         
    
    """
    Function based view which validates ModelForms and returns the updated 
    database table for incomes or spendings depending on the user input. 
    """

    if request.method == 'POST':   
        form = UserModelForm(request.POST)    
        form1 = AddIncome(request.POST)
        if form.is_valid():
  
            u = form.save()
            users = UserDetails.objects.filter(user= request.user).order_by('-date_added')  
            request.user.new_spending.add(u) 

            return render(request, 'budget_app/display.html', {        
                'users': users
                })

        if form1.is_valid():
            x = form1.save()
            users1 = UserIncome.objects.filter(user= request.user).order_by('-date_added')
            request.user.new_income.add(x) 

            return render(request, 'budget_app/display_income.html', {        
                'users1': users1
                })
    else:
        form_class = UserModelForm
        form1_class = AddIncome

        return render(request, 'budget_app/userdetails.html', {
            'form': form_class,
            'form1': form1_class,
            })

class UserDetailsFilterView(FilterView):

    """
    Class based view that calls the year/ month filter on the spendings database 
    and returns the filtered spendings table. 
    """

    filterset_class=BudgetFilter
    template_name='budget_app/history.html'

    def get_queryset(self):
        return UserDetails.objects.filter(user=self.request.user).order_by('-date_added')


def statistics(request, year=date.today().year, month=date.today().month):

    """
    Function based view that returns the current date to be presented on the statistics.html 
    """
    month_name = calendar.month_name[month]
    title_date = f'{month_name} {year}'
    return render(request, "budget_app/statistics.html", {'title_date': title_date})

def line_plot(request, year=date.today().year, month=date.today().month):

    """
    Function based view that creates a line graph plotting the daily spendings for the current month.
    """

    # creating the data to be presented in the graph
    x = []
    y = []
    
    if month == 2: 
        if year % 4 == 0  and  (year % 100 != 0  or  year % 400 == 0):
            days = np.arange(1, 29, 1)
        else: 
            days = np.arange(1, 28, 1)
    elif month in [1, 3, 5, 7, 8, 10, 12]: 
        days = np.arange(1, 31, 1)
    elif month in [4, 6, 9, 11]: 
        days = np.arange(1, 30, 1)

    for day in days: 
        x.append(day)
        y.append(UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, date_added__day=day).aggregate(suma=Sum('cost'))['suma'] or 0.00)

    # creating the figure to plot the graph
    fig = Figure()
    ax = fig.add_subplot(111) 
    
    # creating the axes
    ax.plot(x, y)
    fig.suptitle('Your daily spendings', fontsize=20)
    ax.set(xlabel='day', ylabel='spendings (€)')
    ax.grid()

    # FigureCanvas is the area onto which the figure is drawn
    canvas=FigureCanvas(fig)
    
    # creating the response as image type jpeg
    response=HttpResponse(content_type="image/jpg")
    canvas.print_jpg(response)

    return response


def pie_plot(request, year=date.today().year, month=date.today().month):  
    
    """
    Function based view that creates a donut plot showing the spendings per category for the current month.
    """

    month_name = calendar.month_name[month]

    # creating the figure to plot the graph
    fig = Figure()
    ax = fig.add_subplot(111, aspect='equal')  # equal aspect ratio ensures that pie is drawn as a circle.
    
    wedges = [UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='rent').aggregate(suma=Sum('cost'))['suma']  or 0.00,
    UserDetails.objects.filter(user=request.user,date_added__year=year, date_added__month=month, category='grocery').aggregate(suma=Sum('cost'))['suma'] or 0.00,
    UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='shopping').aggregate(suma=Sum('cost'))['suma'] or 0.00,
    UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='gym').aggregate(suma=Sum('cost'))['suma'] or 0.00,
    UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='phone').aggregate(suma=Sum('cost'))['suma'] or 0.00,
    UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='freetime').aggregate(suma=Sum('cost'))['suma'] or 0.00,
    UserDetails.objects.filter(user=request.user, date_added__year=year, date_added__month=month, category='other').aggregate(suma=Sum('cost'))['suma'] or 0.00]
   
    labels = ['rent', 'grocery', 'shopping', 'gym', 'phone', 'freetime', 'other']    
    def my_autopct(pct):
        return ('%1.1f%%'% pct) if pct > 0.0 else ''    
    ax.pie(wedges, 
    colors=['#ff6666', '#ffcc99', '#99ff99', 'grey', '#c2c2f0', '#66b3ff', '#ffb3e6'],            
    startangle=90, 
    shadow=False, 
    autopct=my_autopct,
    pctdistance=0.55)
    ax.legend(wedges, labels=labels, title='categories', loc='center left', bbox_to_anchor=(0.96, 0, 0.5, 1))
    fig.suptitle('Your spending statistics per category', fontsize=20)

    # draw inner circle for donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    # FigureCanvas is the area onto which the figure is drawn
    canvas=FigureCanvas(fig)

    # creating the response as image type jpeg
    response=HttpResponse(content_type="image/jpg")
    canvas.print_jpg(response)

    return response
