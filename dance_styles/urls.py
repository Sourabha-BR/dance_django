from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'dance_styles'

urlpatterns = [
    # Registration and Payment URLs
    path('register/', views.register_class, name='register'),
    path('payment/<int:registration_id>/', views.payment_view, name='payment'),
    path('payment/<int:registration_id>/confirm/', views.confirm_payment, name='confirm_payment'),
    path('api/dance-style/<int:style_id>/', views.get_dance_style_details, name='dance_style_details'),
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('home/', views.home, name='home'),
    path('style/<int:style_id>/', views.dance_style_detail, name='dance_style_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('instructors/', views.instructors, name='instructors'),
    path('events/', views.events_list, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('my-events/', views.my_events, name='my_events'),
    path('my-classes/', views.my_classes, name='my_classes'),

]
