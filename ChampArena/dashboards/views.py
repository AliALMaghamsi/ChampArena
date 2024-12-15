from django.shortcuts import render , redirect
from django.http import HttpRequest, HttpResponse
from activities.models import Activity,ActivityCategory,ActivityName,ActivityParticipant
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.


def admin_dashboard_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_page_view')
    
    categories=ActivityCategory.objects.all()
    activity_names=ActivityName.objects.all()
    section = request.GET.get('section','activities')
    current_time = now()
    if section == 'activities':
        
        ongoing_activities = Activity.objects.filter(end_date__gte=current_time).order_by('start_date')
        expired_activities = Activity.objects.filter(end_date__lt=current_time).order_by('end_date')
        activities = list(ongoing_activities) + list(expired_activities)
        
        # Filters
        
        #status filter
        status = request.GET.get('status',False)
        if status:
            activities = Activity.objects.filter(status=status)


        #Time filter
        date_filter = request.GET.get('date')
        if date_filter == 'today':
            activities = Activity.objects.filter(created_at__date=now().date())
        elif date_filter == 'last7days':
            activities = Activity.objects.filter(created_at__gte=now() - timedelta(days=7))
        elif date_filter == 'thismonth':
            activities = Activity.objects.filter(created_at__month=now().month)

        #user filter
        user = request.GET.get('user')
        if user:
            activities = Activity.objects.filter(created_by__username__icontains=user)
        
        #title filter
        title =request.GET.get('title')
        if title:
            activities = Activity.objects.filter(title__contains=title)


        page=request.GET.get('page')
        paginator=Paginator(activities,5)
        display=paginator.get_page(page)  
    elif section == 'categories':
        display=ActivityCategory.objects.all()

    else:
        display=None

    
    return render(request,"dashboards/admin_dashboard.html",context={'display':display,'section':section,'categories':categories,'now':current_time})
           
            
       
            
