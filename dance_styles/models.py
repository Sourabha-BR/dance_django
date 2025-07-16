from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.

class DanceStyle(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dance_styles/', null=True, blank=True)
    video = models.FileField(upload_to='dance_videos/', null=True, blank=True)
    choreographer = models.CharField(max_length=100)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class ClassSlot(models.Model):
    dance_style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE, related_name='class_slots')
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.dance_style.name} - {self.day} {self.start_time} to {self.end_time}"

class Registration(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dance_style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE)
    class_slot = models.ForeignKey(ClassSlot, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.dance_style.name}"

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='instructors/', null=True, blank=True)
    bio = models.TextField()
    expertise = models.CharField(max_length=200)
    years_of_experience = models.IntegerField()
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    dance_styles = models.ManyToManyField(DanceStyle, related_name='instructors')

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('competition', 'Competition'),
        ('performance', 'Performance'),
        ('special', 'Special Event'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.PositiveIntegerField(default=50)
    available_slots = models.PositiveIntegerField(default=50)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    dance_styles = models.ManyToManyField(DanceStyle)
    registration_deadline = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_registration_open(self):
        return self.registration_deadline >= timezone.now().date() and self.available_slots > 0

class EventRegistration(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    ticket_number = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

class Video(models.Model):
    VIDEO_TYPES = [
        ('live', 'Live Class'),
        ('recorded', 'Recorded Lesson'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPES)
    dance_style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE, related_name='videos')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)
    video_url = models.URLField(help_text='URL for recorded video or streaming endpoint')
    duration = models.DurationField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_live_now(self):
        if self.video_type == 'live' and self.scheduled_time:
            now = timezone.now()
            # Consider a live class to be active for 2 hours from start time
            return self.scheduled_time <= now <= self.scheduled_time + timezone.timedelta(hours=2)
        return False

class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_duration = models.DurationField(default=timezone.timedelta)
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'video']
    
    def __str__(self):
        return f"{self.user.username} - {self.video.title}"

class VideoComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"
