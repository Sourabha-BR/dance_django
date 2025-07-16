from django.core.management.base import BaseCommand
from django.utils import timezone
from dance_styles.models import Video, DanceStyle, Instructor
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates sample videos for testing'

    def handle(self, *args, **kwargs):
        # Get existing dance styles and instructors
        dance_styles = DanceStyle.objects.all()
        instructors = Instructor.objects.all()

        if not dance_styles.exists():
            self.stdout.write('Please run create_sample_events first to create dance styles')
            return

        if not instructors.exists():
            self.stdout.write('Please create some instructors first')
            return

        # Sample video data
        videos = [
            {
                'title': 'Hip Hop Fundamentals',
                'description': 'Learn the basic moves and techniques of hip hop dancing. Perfect for beginners!',
                'video_type': 'recorded',
                'dance_style': dance_styles.filter(name='Hip Hop').first(),
                'instructor': instructors.first(),
                'video_url': 'https://example.com/videos/hip-hop-fundamentals.mp4',
                'duration': timedelta(minutes=45),
                'is_premium': False
            },
            {
                'title': 'Advanced Contemporary Dance',
                'description': 'Take your contemporary dance skills to the next level with this advanced class.',
                'video_type': 'recorded',
                'dance_style': dance_styles.filter(name='Contemporary').first(),
                'instructor': instructors.first(),
                'video_url': 'https://example.com/videos/advanced-contemporary.mp4',
                'duration': timedelta(minutes=60),
                'is_premium': True
            },
            {
                'title': 'Salsa Dance Workshop',
                'description': 'Join us for a live salsa dance workshop! Learn authentic Latin dance moves.',
                'video_type': 'live',
                'dance_style': dance_styles.filter(name='Salsa').first(),
                'instructor': instructors.first(),
                'video_url': 'https://example.com/live/salsa-workshop',
                'scheduled_time': timezone.now() + timedelta(days=2, hours=3),
                'is_premium': False
            },
            {
                'title': 'Hip Hop Choreography: Level 1',
                'description': 'Learn a complete hip hop dance routine step by step.',
                'video_type': 'recorded',
                'dance_style': dance_styles.filter(name='Hip Hop').first(),
                'instructor': instructors.first(),
                'video_url': 'https://example.com/videos/hip-hop-choreo-1.mp4',
                'duration': timedelta(minutes=30),
                'is_premium': False
            },
            {
                'title': 'Contemporary Flow: Live Session',
                'description': 'Experience the fluidity of contemporary dance in this live class.',
                'video_type': 'live',
                'dance_style': dance_styles.filter(name='Contemporary').first(),
                'instructor': instructors.first(),
                'video_url': 'https://example.com/live/contemporary-flow',
                'scheduled_time': timezone.now() + timedelta(days=1, hours=5),
                'is_premium': True
            }
        ]

        # Create videos
        for video_data in videos:
            video, created = Video.objects.get_or_create(
                title=video_data['title'],
                defaults=video_data
            )
            if created:
                self.stdout.write(f'Created video: {video.title}')
