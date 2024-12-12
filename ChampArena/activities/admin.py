from django.contrib import admin
from .models import Activity, ActivityName,ActivityCategory, ActivityParticipant



class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ActivityNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'status', 'start_date', 'end_date', 'location', 'price_per_person')
    list_filter = ('status', 'created_by', 'start_date', 'end_date')
    search_fields = ('name__name', 'location')
    readonly_fields = ('created_at',)
    list_editable = ('status',)
    actions = ['approve_activity', 'reject_activity']

    def approve_activity(self, request, queryset):
        queryset.update(status='approved')

    def reject_activity(self, request, queryset):
        queryset.update(status='rejected')



admin.site.register(ActivityName,ActivityNameAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(ActivityParticipant)
admin.site.register(ActivityCategory,ActivityCategoryAdmin)
