import os
import tempfile
import requests
from django.db import migrations
from django.core.files import File
from django.conf import settings

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the content type from headers
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                # Create a temporary file
                img_temp = tempfile.NamedTemporaryFile()
                img_temp.write(response.content)
                img_temp.flush()
                return img_temp
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

def add_instructor_images(apps, schema_editor):
    Instructor = apps.get_model('dance_styles', 'Instructor')
    
    # Create media directory if it doesn't exist
    media_root = settings.MEDIA_ROOT
    instructor_images_dir = os.path.join(media_root, 'instructor_images')
    os.makedirs(instructor_images_dir, exist_ok=True)
    
    # Sample image URLs for instructors with proper size parameters
    instructor_images = {
        'Isabella Martinez': 'https://images.unsplash.com/photo-1601288496920-b6154fe3626a?w=800&q=80',
        'James Chen': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80',
        'Aisha Patel': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=800&q=80',
        'Marcus Johnson': 'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=800&q=80',
        'Sofia Petrova': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&q=80'
    }
    
    # Update each instructor with their image
    for instructor in Instructor.objects.all():
        if instructor.name in instructor_images:
            image_url = instructor_images[instructor.name]
            img_temp = download_image(image_url)
            
            if img_temp:
                file_name = f"{instructor.name.lower().replace(' ', '_')}.jpg"
                instructor.profile_image.save(
                    file_name,
                    File(img_temp),
                    save=True
                )
                img_temp.close()

def remove_instructor_images(apps, schema_editor):
    Instructor = apps.get_model('dance_styles', 'Instructor')
    for instructor in Instructor.objects.all():
        if instructor.profile_image:
            instructor.profile_image.delete()

class Migration(migrations.Migration):
    dependencies = [
        ('dance_styles', '0004_add_sample_instructors'),
    ]

    operations = [
        migrations.RunPython(add_instructor_images, remove_instructor_images),
    ]
