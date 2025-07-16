import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from dance_styles.models import DanceStyle

class Command(BaseCommand):
    help = 'Add dance styles with images'

    def handle(self, *args, **options):
        # List of dance styles with their details
        dance_styles = [
            {
                'name': 'Hip Hop',
                'image_url': 'https://images.unsplash.com/photo-1535525153412-5a42439a210d',
                'choreographer': 'Alex Thompson',
                'registration_fee': 2500.00,
                'description': 'Urban dance style that includes a variety of styles and elements, focusing on rhythm, body movements, and freestyle.',
            },
            {
                'name': 'Ballet',
                'image_url': 'https://images.unsplash.com/photo-1518834107812-67b0b7c58434',
                'choreographer': 'Maria Rodriguez',
                'registration_fee': 3000.00,
                'description': 'Classical dance form characterized by grace, precision, and fluidity of movement.',
            },
            {
                'name': 'Contemporary',
                'image_url': 'https://images.unsplash.com/photo-1545016803-a7e357a737e4',
                'choreographer': 'Sarah Chen',
                'registration_fee': 2800.00,
                'description': 'Modern dance style that combines elements of several dance genres including modern, jazz, lyrical, and classical ballet.',
            },
            {
                'name': 'Salsa',
                'image_url': 'https://images.unsplash.com/photo-1545959570-a94084071b5d',
                'choreographer': 'Carlos Mendoza',
                'registration_fee': 2200.00,
                'description': 'Latin dance style known for its energetic movements and intricate partner work.',
            },
        ]

        for style_data in dance_styles:
            try:
                # Check if dance style already exists
                if DanceStyle.objects.filter(name=style_data['name']).exists():
                    self.stdout.write(self.style.WARNING(f"{style_data['name']} already exists"))
                    continue

                # Create dance style
                dance_style = DanceStyle.objects.create(
                    name=style_data['name'],
                    choreographer=style_data['choreographer'],
                    registration_fee=style_data['registration_fee'],
                    description=style_data['description']
                )

                # Download and save image
                response = requests.get(style_data['image_url'])
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()

                    # Save image to dance style
                    filename = f"{style_data['name'].lower().replace(' ', '_')}.jpg"
                    dance_style.image.save(filename, File(img_temp), save=True)
                    self.stdout.write(self.style.SUCCESS(f"Successfully added {style_data['name']} with image"))
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to download image for {style_data['name']}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding {style_data['name']}: {str(e)}"))
