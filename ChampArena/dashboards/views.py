from django.shortcuts import render , redirect
from django.http import HttpRequest, HttpResponse
from activities.models import Activity,ActivityCategory,ActivityName,ActivityParticipant
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def admin_dashboard_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_page_view')
    
    section = request.GET.get('section','activities')
    if section == 'activities':
        activities= Activity.objects.all()
        page=request.GET.get('page')
        paginator=Paginator(activities,3)
        display=paginator.get_page(page)  
    else:
            display=None

    
    return render(request,"dashboards/admin_dashboard.html",context={'display':display,'section':section})
           
            
       
            
