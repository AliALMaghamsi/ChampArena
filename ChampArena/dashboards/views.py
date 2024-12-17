from django.shortcuts import render , redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from activities.models import Activity,ActivityCategory,ActivityName,ActivityParticipant,Booking,Notification
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
            activities = Activity.objects.filter(created_by__username__icontains=user).order_by('-start_date')
        
        #title filter
        title =request.GET.get('title')
        if title:
            activities = Activity.objects.filter(title__contains=title).order_by('-start_date')

        category=request.GET.get('category')
        if category:
            activities = Activity.objects.filter(name__category__id=category).order_by('-start_date')

        activity_name=request.GET.get('name')
        if activity_name:
            activities = Activity.objects.filter(name__id=activity_name).order_by('-start_date')

        page=request.GET.get('page')
        paginator=Paginator(activities,5)
        display=paginator.get_page(page)  
    elif section == 'categories':
        display=ActivityCategory.objects.all()

    else:
        display=None

    
    return render(request,"dashboards/admin_dashboard.html",context={'display':display,'section':section,'categories':categories,'now':current_time})
           
            
       
def user_dashboard_view(request):
 
    activities = Activity.objects.filter(created_by=request.user)

   
    bookings = Booking.objects.filter(activity__in=activities)

    
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()

   
    unread_notifications = request.user.notifications.filter(is_read=False)
    if unread_notifications.exists():
        unread_notifications.update(is_read=True)

    if request.method == "POST":
        action = request.POST.get('action')
        booking_id = request.POST.get('booking_id')

        if booking_id:
            try:
                booking = get_object_or_404(Booking, id=booking_id, activity__in=activities)
                
                if action == "accept":
                    booking.status = "Completed"
                    booking.save()

                 
                    notification_message = f"Your booking for {booking.activity.name} has been accepted."
                    Notification.objects.create(user=booking.user, message=notification_message)

                    messages.success(request, "The request accepted successfully", 'alert-success')

                elif action == "reject":
                    booking.status = "Cancelled"
                    booking.delete()  
                    notification_message = f"Your booking for {booking.activity.name} has been rejected."
                    Notification.objects.create(user=booking.user, message=notification_message)

                else:
                    return render(request, 'dashboards/user_dashboard.html', {
                        'activities': activities,
                        'bookings': bookings,
                        'error': 'Invalid action.',
                        'unread_notifications_count': unread_notifications_count,
                    })

                return redirect('user_dashboard_view')

            except Exception as e:
                return render(request, 'dashboards/user_dashboard.html', {
                    'activities': activities,
                    'bookings': bookings,
                    'error': f"An error occurred: {str(e)}",
                    'unread_notifications_count': unread_notifications_count,
                })
        else:
            return render(request, 'dashboards/user_dashboard.html', {
                'activities': activities,
                'bookings': bookings,
                'error': 'Booking ID is missing.',
                'unread_notifications_count': unread_notifications_count,
            })

    return render(request, 'dashboards/user_dashboard.html', {'activities': activities,'bookings': bookings,'unread_notifications_count': unread_notifications_count, })

# حذف الإشعار
def delete_notification_view(request:HttpRequest, notification_id):
    try:
        # استعلام الإشعار باستخدام المعرف
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)

        # حذف الإشعار
        notification.delete()

        messages.success(request, "Notification deleted.")

    except Notification.DoesNotExist:
        messages.error(request, "Notification not found.")

 
    next_url = request.GET.get('next', 'user_dashboard_view') 
    return HttpResponseRedirect(next_url)