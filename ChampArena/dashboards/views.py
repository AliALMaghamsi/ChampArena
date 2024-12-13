from django.shortcuts import render , redirect
from django.http import HttpRequest, HttpResponse
from activities.models import Activity,ActivityCategory,ActivityName,ActivityParticipant
from django.contrib import messages
# Create your views here.


def admin_dashboard_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_page_view')
    # section = request.GET.get('section') or request.POST.get('section', 'projects')

    # if section == 'activities':
                    
    #                 if "search" in request.GET :
    #                     projects= Project.objects.filter(title__contains=request.GET["search"])
    #                 elif "order_by" in request.GET and request.GET["order_by"]=="category":
    #                     projects=Project.objects.filter().order_by("-category")
    #                 elif "order_by" in request.GET and request.GET["order_by"]=="completed_date":
    #                     projects=Project.objects.filter().order_by("-completed_date")
    #                 else:
    #                     projects = Project.objects.all()

    #                 page=request.GET.get('page')
    #                 paginator=Paginator(projects,2)
    #                 display=paginator.get_page(page)  
                      
                    
    # elif section == 'messages':
                    
    #                 contacts=Contact.objects.all()
    #                 page=request.GET.get('page')
    #                 paginator=Paginator(contacts,3)
    #                 display=paginator.get_page(page) 
    # else:
    #                 display=None
    return render(request,"dashboards/admin_dashboard.html",)
           
            
       
            
