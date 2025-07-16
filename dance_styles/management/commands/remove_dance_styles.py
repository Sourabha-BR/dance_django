from django.core.management.base import BaseCommand
from dance_styles.models import DanceStyle

class Command(BaseCommand):
    help = 'Remove specified dance styles'

    def handle(self, *args, **options):
        styles_to_remove = ['Street Jazz', 'Waltz', 'Tango']
        
        for style_name in styles_to_remove:
            try:
                style = DanceStyle.objects.filter(name__iexact=style_name)
                if style.exists():
                    style.delete()
                    self.stdout.write(self.style.SUCCESS(f'Successfully removed {style_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'{style_name} not found'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error removing {style_name}: {str(e)}'))
