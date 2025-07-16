from django.core.management.base import BaseCommand
from django.utils import timezone
from dance_styles.models import Event, DanceStyle
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates sample events for testing'

    def handle(self, *args, **kwargs):
        # Create some dance styles if they don't exist
        dance_styles = [
            {
                'name': 'Hip Hop',
                'description': 'Urban street dance style',
                'choreographer': 'Mike Johnson',
                'registration_fee': 50.00
            },
            {
                'name': 'Contemporary',
                'description': 'Modern expressive dance',
                'choreographer': 'Sarah Williams',
                'registration_fee': 60.00
            },
            {
                'name': 'Salsa',
                'description': 'Latin partner dance',
                'choreographer': 'Carlos Rodriguez',
                'registration_fee': 45.00
            }
        ]

        created_styles = []
        for style_data in dance_styles:
            style, created = DanceStyle.objects.get_or_create(
                name=style_data['name'],
                defaults=style_data
            )
            created_styles.append(style)
            if created:
                self.stdout.write(f'Created dance style: {style.name}')

        # Create upcoming events
        today = timezone.now().date()
        events = [
            {
                'title': 'Summer Dance Workshop 2025',
                'event_type': 'workshop',
                'description': 'Join us for an intensive summer dance workshop featuring multiple dance styles and expert instructors.',
                'date': today + timedelta(days=15),
                'time': '14:00',
                'location': 'Main Studio Hall',
                'price': 99.99,
                'capacity': 30,
                'available_slots': 30,
                'registration_deadline': today + timedelta(days=10),
                'is_featured': True
            },
            {
                'title': 'Dance Competition: Battle of Styles',
                'event_type': 'competition',
                'description': 'Annual dance competition showcasing various dance styles. Cash prizes for winners!',
                'date': today + timedelta(days=30),
                'time': '18:00',
                'location': 'Grand Auditorium',
                'price': 49.99,
                'capacity': 50,
                'available_slots': 50,
                'registration_deadline': today + timedelta(days=25),
                'is_featured': True
            },
            {
                'title': 'Street Dance Special Workshop',
                'event_type': 'workshop',
                'description': 'Learn the latest street dance moves and techniques in this special workshop.',
                'date': today + timedelta(days=7),
                'time': '16:00',
                'location': 'Studio B',
                'price': 39.99,
                'capacity': 20,
                'available_slots': 20,
                'registration_deadline': today + timedelta(days=5),
                'is_featured': False
            },
            {
                'title': 'Dance Showcase 2025',
                'event_type': 'performance',
                'description': 'Annual showcase featuring performances from our students and instructors.',
                'date': today + timedelta(days=45),
                'time': '19:00',
                'location': 'City Theater',
                'price': 29.99,
                'capacity': 100,
                'available_slots': 100,
                'registration_deadline': today + timedelta(days=40),
                'is_featured': True
            }
        ]

        for event_data in events:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                # Add dance styles to the event
                event.dance_styles.add(*created_styles)
                self.stdout.write(f'Created event: {event.title}')
            else:
                self.stdout.write(f'Event already exists: {event.title}')
