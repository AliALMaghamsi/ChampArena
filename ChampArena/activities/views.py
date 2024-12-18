from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from .forms import ActivityForm,ActivityCategoryForm,ActivityNameForm,ReviewForm
from .models import Activity, ActivityName, ActivityCategory,Booking,Notification,Review
from django.utils import timezone

import anthropic
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def moderate_content_with_claude(title: str, description: str) -> bool:
    """
    Use Claude to check if content is inappropriate in both English and Arabic.
    Returns True if content is clean, False if inappropriate.
    """
    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        # Multilingual content moderation prompt
        prompt = f"""You are a multilingual content moderator. Carefully review the following text for any potentially inappropriate, offensive, or problematic content in both Arabic and English:

Title: {title}
Description: {description}

Evaluation Criteria:
1. Check for offensive language or hate speech in Arabic and English
2. Look for inappropriate content, including:
   - Explicit or vulgar language
   - Threats or harassment
   - Discriminatory remarks
   - Inappropriate references
3. Consider cultural sensitivities in both Arabic and English contexts

Respond STRICTLY with:
- 'CLEAN' if the content is completely appropriate in both languages
- 'NOT_CLEAN' if there are any concerns about the content

Your response must be either 'CLEAN' or 'NOT_CLEAN'. Be very strict in your evaluation and consider nuances in both Arabic and English languages."""

        response = client.messages.create(
            model="claude-3-sonnet-20240229",  # Using a more capable model for multilingual content
            max_tokens=150,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and parse the response more robustly
        moderation_result = response.content[0].text.strip().upper()
        
        # Print the raw response for debugging
        print(f"Raw moderation response: {moderation_result}")
        
        # Check for the specific response
        return moderation_result == 'CLEAN'
    
    except Exception as e:
        # Use proper logging instead of print
        logger.error(f"Content moderation error: {e}")
        # In case of any error, default to not approving
        return False

def new_activity_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in first!", "alert-warning")
        return redirect("main:home_page_view")

    today = datetime.now().strftime('%Y-%m-%dT%H:%M')
    activity_form = ActivityForm()  
    activity_categories = ActivityCategory.objects.all()
    activity_names = ActivityName.objects.none()

    if request.method == "POST":
        try:
            activity_form = ActivityForm(request.POST, request.FILES)
            if activity_form.is_valid():
                activity :Activity = activity_form.save(commit=False)
                activity.created_by = request.user
                
                # Get title and description directly from form
                title = activity_form.cleaned_data.get('title', '')
                description = activity_form.cleaned_data.get('description', '')
                
                is_content_clean = moderate_content_with_claude(
                    title=title, 
                    description=description
                )
                
                if is_content_clean:
                    activity.status = 'approved'  
                    messages.success(request, "Created and approved activity successfully!", "alert-success")
                else:
                   
                    messages.warning(request, "Activity requires manual review.", "alert-warning")
                
                activity.save()
                return redirect("dashboards:user_dashboard_view")
            else:
                # Log form errors
                logger.error(f"Form errors: {activity_form.errors}")
                messages.error(request, "There was an error with your form. Please try again.", "alert-danger")
        except Exception as e:
            # Log the full exception
            logger.error(f"Unexpected error: {e}", exc_info=True)
            messages.error(request, "An unexpected error occurred.", "alert-danger")

    return render(request, "activities/new_activity.html", context={
        "form": activity_form,
        "categories": activity_categories,
        "activities_name": activity_names,
        "today": today
    })

def update_activity_view(request:HttpRequest, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if not request.user == activity.created_by:
        messages.warning(request, "Access Denid! This is not your Activity", "alert-warning")
        return redirect("main:home_page_view")
    categories = ActivityCategory.objects.all()
    activity_names = ActivityName.objects.none()
    if request.method == 'POST':
        try:
            form = ActivityForm(request.POST,request.FILES, instance=activity)
            
            if form.is_valid():
                
                activity :Activity = form.save(commit=False)
                title = form.cleaned_data.get('title', '')
                description = form.cleaned_data.get('description', '')

                is_content_clean = moderate_content_with_claude(
                    title=title, 
                    description=description
                )
                
                if is_content_clean:
                    activity.status = 'approved'  
                    messages.success(request, "Created and approved activity successfully!", "alert-success")
                    
                else:
                    activity.status = 'in_review'  
                    messages.warning(request, "Activity requires manual review.", "alert-warning")

                form.save()
                
                return redirect("dashboards:user_dashboard_view")
            else:
                messages.error(request, 'There was an error updating the activity.')
        except Exception as e:
            print(e)
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'activities/update_activity.html', {
        'form': form,
        'activity': activity,
        'categories': categories,
        "activities_name": activity_names,
    })


def get_activities(request:HttpRequest, category_id):
    activities = ActivityName.objects.filter(category_id=category_id)
    return JsonResponse({'activities': list(activities.values('id', 'name'))})


def detail_activity_view(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    current_date = timezone.now()
    reviews = Review.objects.filter(activity=activity) if activity.end_date < current_date else []

    has_booked = Booking.objects.filter(user=request.user, activity=activity, status__in=['Booked', 'Completed']).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if has_booked:
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.instance.activity = activity
                form.instance.user = request.user
                form.save()
                return redirect('activities:detail_activity_view', activity_id=activity.id)
        else:
            return redirect('activities:detail_activity_view', activity_id=activity.id)

    else:
        form = ReviewForm()

    return render(request, "activities/activity_detail.html", {
        "activities": activity,
        "reviews": reviews,
        "form": form,
        "has_booked": has_booked
    })
def all_activities_view(request : HttpRequest):
    activities = Activity.objects.filter(status='approved').order_by('start_date')
    activities_category=ActivityCategory.objects.all()
    activities_name=ActivityName.objects.none()
    
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        activities = Activity.objects.filter(title__contains=request.GET["search"])
        
    if "category" in request.GET and request.GET["category"]:

        activities = activities.filter(name__category__id=request.GET["category"])

    if "name" in request.GET and request.GET["name"]:
        activities = activities.filter(name__id=request.GET["name"])

    page_number = request.GET.get("page")  
    paginator = Paginator(activities,4)
    activities_page = paginator.get_page(page_number)
    return render(request,"activities/all_activities.html",context={"activities":activities_page,'categories':activities_category,'activities_name':activities_name})



def book_activity(request: HttpRequest, activity_id: int):
    activity = Activity.objects.get(id=activity_id)
    user_profile = request.user.profile
    
    if Booking.objects.filter(user=request.user, activity=activity).exists():
        messages.error(request, 'You have already booked this activity.', 'alert-warning')
        return redirect('activities:all_activities_view')  

    if user_profile.wallet_balance >= activity.price_per_person:
        user_profile.wallet_balance -= activity.price_per_person
        user_profile.save()

        booking = Booking.objects.create(
            user=request.user,
            activity=activity,
            amount=activity.price_per_person,
            status='Booked'
        )

       
        messages.success(request, 'Booking successful! The host has been notified.', 'alert-success')
        return redirect('accounts:profile')  
    else:
        messages.error(request, 'Insufficient wallet balance to book this activity.', 'alert-danger')
        return redirect('activities:detail_activity_view', activity_id=activity.id)


def new_category_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid!", "alert-warning")
        return redirect("main:home_page_view")
    
    activity_category_form = ActivityCategoryForm()  
    if request.method == "POST":
        try:
            
            activity_category_form=ActivityCategoryForm(request.POST)
            if activity_category_form.is_valid():
                activity_category_form.save()
                messages.success(request, "Created Category successfully!", "alert-success")
                return redirect(request.GET.get('section','/'))
            else:
                messages.error(request, f"{activity_category_form.errors.get('name', None)[0]}. Please try again.", "alert-danger")
                return redirect(request.GET.get('section','/'))
        except Exception as e:
            messages.error(request, "something went wrong", "alert-danger")

def update_category_view(request:HttpRequest, category_id:int):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid! ", "alert-warning")
        return redirect("main:home_page_view")
    category = ActivityCategory.objects.get(pk=category_id)
    if request.method=="POST":
        try:
            category.name=request.POST['name']
            category.save()
            messages.success(request, "updated Category successfully!", "alert-success")
            return redirect(request.GET.get('section','/'))
        except Exception as e:
            print(e)
    return redirect
  
def delete_category_view(request:HttpRequest , category_id:int):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid! ", "alert-warning")
        return redirect("main:home_page_view")
    category = ActivityCategory.objects.get(pk=category_id)
    if request.method=="POST":
        try:
            category.delete()
            messages.success(request, "Deleted Category successfully!", "alert-success")
            return redirect(request.GET.get('section','/'))
        except Exception as e:
            print(e)

def new_activity_name_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid!", "alert-warning")
        return redirect("main:home_page_view")
    
    activity_name_form = ActivityNameForm()  
    if request.method == "POST":
        try:
            
            activity_name_form=ActivityNameForm(request.POST)
            if activity_name_form.is_valid():
                activity_name_form.save()
                messages.success(request, "Created Activity Name successfully!", "alert-success")
                return redirect(request.GET.get('section','/'))
            else:
                messages.error(request, f"{activity_name_form.errors.get('name', None)[0]}. Please try again.", "alert-danger")
                return redirect(request.GET.get('section','/'))
        except Exception as e:
            messages.error(request, "something went wrong", "alert-danger")

def update_activity_name_view(request:HttpRequest, activity_id:int):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid! ", "alert-warning")
        return redirect("main:home_page_view")
    activity_name = ActivityName.objects.get(pk=activity_id)
    if request.method=="POST":
        try:
            activity_name.name=request.POST['name']
            activity_name.save()
            messages.success(request, "updated Activity Name successfully!", "alert-success")
            return redirect(request.GET.get('section','/'))
        except Exception as e:
            print(e)
    return redirect
  
def delete_activity_name_view(request:HttpRequest , activity_id:int):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid! ", "alert-warning")
        return redirect("main:home_page_view")
    activity_name = ActivityName.objects.get(pk=activity_id)
    if request.method=="POST":
        try:
            activity_name.delete()
            messages.success(request, "Deleted Activity Name successfully!", "alert-success")
            return redirect(request.GET.get('section','/'))
        except Exception as e:
            print(e)


    

def activity_status(request:HttpRequest,activity_id:int):
    if not request.user.is_staff:
        messages.warning(request, "Access Denid!", "alert-warning")
        return redirect("main:home_page_view")
    activity=Activity.objects.get(pk = activity_id)
    
    if request.method == 'POST':
        try:
            activity.status=request.POST['status']
            activity.save()
            return redirect('dashboards:admin_dashboard_view')
        except Exception as e :
            print(e)