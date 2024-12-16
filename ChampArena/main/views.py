from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse

from .models import ContactMessage

from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.


def home_page_view(request:HttpRequest):
    

    return render(request, 'main/index.html')




def about_page_view(request:HttpRequest):
    

    return render(request,"main/about.html")





def contact_page_view(request:HttpRequest):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Save the contact message for logged-in user
            contact = ContactMessage(
                first_name=request.user.first_name,  # Use the logged-in user's first name
                last_name=request.user.last_name,    # Use the logged-in user's last name
                topic=request.POST["topic"],
                title=request.POST["title"],
                email=request.user.email,            # Use the logged-in user's email
                message=request.POST["message"]
            )
        else:
            # Save the contact message for non-logged-in user
            contact = ContactMessage(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                topic=request.POST["topic"],
                title=request.POST["title"],
                email=request.POST["email"],
                message=request.POST["message"]
            )
        contact.save()

        # Render the HTML email template
        email_body = render_to_string("main/contact_messages.html", {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "topic": contact.topic,
            "title":contact.title,
            "message": contact.message,
            "email": contact.email
        })
        messages.success(request, "Your message is received. Thank you.", "alert-success")
        # Send the email
        admin_email = settings.EMAIL_HOST_USER 
        email_message = EmailMessage(
            subject=f"{contact.title}:{contact.topic}",
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[admin_email]  # Email is sent to admin/support team only
        )
        email_message.content_subtype = "html"  # Specify that the email is HTML
        email_message.send()
        
        
         

    return render(request, 'main/contact.html')