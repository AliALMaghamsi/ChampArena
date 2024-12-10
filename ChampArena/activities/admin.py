from django.contrib import admin
from .models import Activity, ActivityName, ActivityParticipant

admin.site.register(ActivityName)
admin.site.register(Activity)
admin.site.register(ActivityParticipant)
