from django.db import migrations
from random import uniform

def update_prices(apps, schema_editor):
    Event = apps.get_model('dance_styles', 'Event')
    for event in Event.objects.all():
        # Generate a random price between 2000 and 4000
        event.price = round(uniform(2000, 4000), 2)
        event.save()

def revert_prices(apps, schema_editor):
    Event = apps.get_model('dance_styles', 'Event')
    for event in Event.objects.all():
        event.price = 29.99  # Default price
        event.save()

class Migration(migrations.Migration):
    dependencies = [
        ('dance_styles', '0007_rename_end_time_event_time_and_more'),
    ]

    operations = [
        migrations.RunPython(update_prices, revert_prices),
    ]
