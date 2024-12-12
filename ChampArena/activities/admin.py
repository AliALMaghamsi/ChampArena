from django.contrib import admin
from .models import Activity, ActivityName,ActivityCategory, ActivityParticipant



admin.site.register(ActivityName)
admin.site.register(Activity)
admin.site.register(ActivityParticipant)
admin.site.register(ActivityCategory)
