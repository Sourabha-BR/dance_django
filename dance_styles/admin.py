from django.contrib import admin
from .models import DanceStyle, ClassSlot, Registration, Instructor, Event, EventRegistration

# Register your models here.

class ClassSlotInline(admin.TabularInline):
    model = ClassSlot
    extra = 2

@admin.register(DanceStyle)
class DanceStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'choreographer', 'registration_fee', 'video')
    search_fields = ('name', 'choreographer')
    inlines = [ClassSlotInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'choreographer', 'description')
        }),
        ('Media', {
            'fields': ('image', 'video')
        }),
        ('Details', {
            'fields': ('registration_fee',)
        }),
    )

@admin.register(ClassSlot)
class ClassSlotAdmin(admin.ModelAdmin):
    list_display = ('dance_style', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'dance_style')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'dance_style', 'registration_date', 'payment_status')
    list_filter = ('payment_status', 'dance_style')
    search_fields = ('user__username', 'dance_style__name')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'expertise', 'years_of_experience')
    search_fields = ('name', 'expertise')
    filter_horizontal = ('dance_styles',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'price', 'available_slots', 'registration_deadline')
    list_filter = ('event_type', 'is_featured', 'dance_styles')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('dance_styles',)
    date_hierarchy = 'date'

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user', 'event', 'registration_date', 'payment_status')
    list_filter = ('payment_status', 'registration_date')
    search_fields = ('ticket_number', 'user__username', 'event__title')
    readonly_fields = ('ticket_number',)
