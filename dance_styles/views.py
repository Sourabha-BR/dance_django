from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import DanceStyle, ClassSlot, Registration, Event, EventRegistration, Instructor
from datetime import timedelta

# Create your views here.
from .models import DanceStyle, ClassSlot, Registration

@login_required
def register_class(request):
    # Get the dance style from query parameters if it's a GET request
    dance_style_id = request.GET.get('dance_style') or request.POST.get('dance_style')
    if not dance_style_id:
        return redirect('dance_styles:home')
    
    dance_style = get_object_or_404(DanceStyle, id=dance_style_id)
    
    if request.method == 'POST':
        class_slot_id = request.POST.get('class_slot')
        name = request.POST.get('name')
        
        if class_slot_id and name:
            class_slot = get_object_or_404(ClassSlot, id=class_slot_id)
            
            # Update user's name
            request.user.first_name = name
            request.user.save()
            
            # Create registration
            registration = Registration.objects.create(
                user=request.user,
                dance_style=dance_style,
                class_slot=class_slot
            )
            
            return redirect('dance_styles:payment', registration_id=registration.id)
    
    return render(request, 'dance_styles/register.html', {
        'dance_style': dance_style,
        'user': request.user
    })

@login_required
def payment_view(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    return render(request, 'dance_styles/payment.html', {'registration': registration})

@login_required
def confirm_payment(request, registration_id):
    if request.method == 'POST':
        registration = get_object_or_404(Registration, id=registration_id, user=request.user)
        registration.payment_status = 'completed'
        registration.save()
        messages.success(request, 'Payment confirmed! Welcome to the dance class!')
        return redirect('dance_styles:home')

def get_dance_style_details(request, style_id):
    dance_style = get_object_or_404(DanceStyle, id=style_id)
    class_slots = dance_style.class_slots.all()
    
    return JsonResponse({
        'choreographer': dance_style.choreographer,
        'registration_fee': str(dance_style.registration_fee),
        'class_slots': [
            {
                'id': slot.id,
                'day': slot.day,
                'start_time': slot.start_time.strftime('%I:%M %p'),
                'end_time': slot.end_time.strftime('%I:%M %p')
            } for slot in class_slots
        ]
    })

@login_required(login_url='dance_styles:login')
def home(request):
    """
    Home page view that displays all dance styles (dashboard)
    """
    dance_styles = DanceStyle.objects.all()
    return render(request, 'dance_styles/home.html', {'dance_styles': dance_styles})

@login_required(login_url='dance_styles:login')
def dance_style_detail(request, style_id):
    """
    Detail view for a specific dance style
    """
    dance_style = get_object_or_404(DanceStyle, id=style_id)
    return render(request, 'dance_styles/dance_style_detail.html', {'dance_style': dance_style})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dance_styles:home')
        else:
            return render(request, 'dance_styles/login.html', {'error': 'Invalid username or password'})
    return render(request, 'dance_styles/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'dance_styles/signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'dance_styles/signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('dance_styles:home')
    return render(request, 'dance_styles/signup.html')

def about(request):
    """About Us page view"""
    return render(request, 'dance_styles/about.html')

def instructors(request):
    """Instructors page view"""
    instructors = Instructor.objects.all().prefetch_related('dance_styles')
    return render(request, 'dance_styles/instructors.html', {'instructors': instructors})

def contact(request):
    """Contact Us page view with form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Email content
        email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        try:
            # Send email
            send_mail(
                subject,
                email_message,
                email,  # From email
                ['info@dancestudio.com'],  # To email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('dance_styles:contact')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
    
    return render(request, 'dance_styles/contact.html')

def logout_view(request):
    logout(request)
    return redirect('dance_styles:login')

def events_list(request):
    featured_events = Event.objects.filter(is_featured=True, date__gte=timezone.now().date()).order_by('date')[:3]
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now().date()).order_by('-date')[:5]
    
    context = {
        'featured_events': featured_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'dance_styles/events.html', context)

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    
    if request.method == 'POST' and not user_registered and event.is_registration_open():
        # Create event registration
        registration = EventRegistration.objects.create(
            user=request.user,
            event=event,
            payment_status='pending'
        )
        # Decrease available slots
        event.available_slots -= 1
        event.save()
        
        messages.success(request, f'Successfully registered for {event.title}! Your ticket number is {registration.ticket_number}')
        return redirect('dance_styles:event_detail', event_id=event.id)
    
    context = {
        'event': event,
        'user_registered': user_registered,
    }
    return render(request, 'dance_styles/event_detail.html', context)

@login_required
def my_classes(request):
    class_registrations = Registration.objects.filter(user=request.user).select_related('dance_style', 'class_slot').order_by('-registration_date')
    context = {
        'registrations': class_registrations,
    }
    return render(request, 'dance_styles/my_classes.html', context)

@login_required
def my_events(request):
    user_registrations = EventRegistration.objects.filter(user=request.user).select_related('event').order_by('event__date')
    
    upcoming_events = []
    past_events = []
    today = timezone.now().date()

    for reg in user_registrations:
        if reg.event.date >= today:
            upcoming_events.append(reg)
        else:
            past_events.append(reg)

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'dance_styles/my_events.html', context)
