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
        
        page=request.GET.get('page')
        paginator=Paginator(categories,6)
        display=paginator.get_page(page)

    elif section == 'activity_names':
        
        page=request.GET.get('page')
        paginator=Paginator(activity_names,8)
        display=paginator.get_page(page)  

    else:
        display=None

    
    return render(request,"dashboards/admin_dashboard.html",context={'display':display,'section':section,'categories':categories,'now':current_time})
           
            
       
def user_dashboard_view(request):
    # Get all activities created by the logged-in user
    activities = Activity.objects.filter(created_by=request.user)
    
    # Filter bookings based on selected activity (if provided)
    activity_id = request.GET.get('activity_id')  # Get the activity ID from the request
    if activity_id:
        selected_activity = get_object_or_404(activities, id=activity_id)
        bookings = Booking.objects.filter(activity=selected_activity)
    else:
        selected_activity = None
        bookings = Booking.objects.filter(activity__in=activities)
    
    # Get activities booked by the logged-in user
    booked_activities = Booking.objects.filter(user=request.user).select_related('activity')

    # Count unread notifications
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    unread_notifications = request.user.notifications.filter(is_read=False)
    if unread_notifications.exists():
        unread_notifications.update(is_read=True)

    # Handle POST requests for Accept/Reject actions
    if request.method == "POST":
        action = request.POST.get('action')
        booking_id = request.POST.get('booking_id')

        if booking_id:
            try:
                booking = get_object_or_404(Booking, id=booking_id, activity__in=activities)
                if action == "accept":
                    booking.status = "Completed"
                    booking.save()

                    # Send notification to the user
                    notification_message = f"Your booking for {booking.activity.name} has been accepted."
                    Notification.objects.create(user=booking.user, message=notification_message)
                    messages.success(request, "The request was accepted successfully.", 'alert-success')

                elif action == "reject":
                    booking.status = "Cancelled"
                    booking.delete()

                    notification_message = f"Your booking for {booking.activity.name} has been rejected."
                    Notification.objects.create(user=booking.user, message=notification_message)
                    messages.success(request, "The request was rejected successfully.", 'alert-danger')

                return redirect('dashboards:user_dashboard_view')

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}", 'alert-danger')
    
    context = {
        'activities': activities,
        'selected_activity': selected_activity,
        'bookings': bookings,
        'booked_activities': booked_activities,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'dashboards/user_dashboard.html', context)
def delete_notification_view(request:HttpRequest, notification_id):
    try:
       
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)

        notification.delete()

        messages.success(request, "Notification deleted.")

    except Notification.DoesNotExist:
        messages.error(request, "Notification not found.")

 
    next_url = request.GET.get('next', 'user_dashboard_view') 
    return HttpResponseRedirect(next_url)


