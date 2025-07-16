from django.core.management.base import BaseCommand
from dance_styles.models import Event
from random import uniform

class Command(BaseCommand):
    help = 'Updates event prices to be between 2000 and 4000'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        for event in events:
            event.price = round(uniform(2000, 4000), 2)
            event.save()
            self.stdout.write(f'Updated {event.title} price to ₹{event.price}')
