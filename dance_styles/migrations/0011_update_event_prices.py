from django.db import migrations
from decimal import Decimal

def update_event_prices(apps, schema_editor):
    Event = apps.get_model('dance_styles', 'Event')
    
    # Sample event data with updated prices
    events_data = [
        {
            'title': 'Dance Competition: Battle of Styles',
            'price': Decimal('2999.00'),
            'event_type': 'competition',
            'location': 'Grand Auditorium'
        },
        {
            'title': 'Hip Hop Workshop',
            'price': Decimal('2499.00'),
            'event_type': 'workshop',
            'location': 'Studio A'
        },
        {
            'title': 'Summer Dance Festival',
            'price': Decimal('3499.00'),
            'event_type': 'special',
            'location': 'Main Hall'
        },
        {
            'title': 'Contemporary Dance Showcase',
            'price': Decimal('2799.00'),
            'event_type': 'performance',
            'location': 'Theatre Hall'
        }
    ]
    
    # Update existing events or create new ones
    for event_data in events_data:
        Event.objects.update_or_create(
            title=event_data['title'],
            defaults={
                'price': event_data['price'],
                'event_type': event_data['event_type'],
                'location': event_data['location']
            }
        )

def revert_event_prices(apps, schema_editor):
    Event = apps.get_model('dance_styles', 'Event')
    Event.objects.all().update(price=Decimal('29.99'))

class Migration(migrations.Migration):
    dependencies = [
        ('dance_styles', '0010_video_videocomment_videoprogress'),
    ]

    operations = [
        # migrations.RunPython(update_event_prices, revert_event_prices),
    ]
