from django.core.management.base import BaseCommand
from dance_styles.models import DanceStyle, ClassSlot
from django.utils.timezone import datetime

class Command(BaseCommand):
    help = 'Loads sample dance styles and class slots data'

    def handle(self, *args, **kwargs):
        # First, clear existing data
        self.stdout.write('Clearing existing data...')
        DanceStyle.objects.all().delete()
        
        # Create dance styles
        self.stdout.write('Creating dance styles...')
        
        # Hip Hop
        hip_hop = DanceStyle.objects.create(
            name='Hip Hop',
            choreographer='Alex Johnson',
            registration_fee=2500.00,
            description="""Hip hop dance is a vibrant form of dance that combines a variety of freestyle movements to create a cultural experience. 
            Born in the 1970s in New York, it evolved from break dancing and funk styles. 
            Our classes focus on rhythm, body isolations, footwork, and choreography to popular music. 
            Students will learn the fundamentals of hip hop movement, popping, locking, and breaking. 
            This high-energy class is perfect for beginners and experienced dancers alike."""
        )
        
        # Contemporary
        contemporary = DanceStyle.objects.create(
            name='Contemporary',
            choreographer='Emily Roberts',
            registration_fee=3000.00,
            description="""Contemporary dance is a style of expressive dance that combines elements of several dance genres including modern, jazz, lyrical and classical ballet. 
            Our classes emphasize versatility and improvisation, with focus on floor work, fall and recovery, and contract and release. 
            Students will develop strong technical skills while learning to use dance as a means of self-expression. 
            This class encourages dancers to explore their creativity and emotional depth through movement."""
        )
        
        # Ballet
        ballet = DanceStyle.objects.create(
            name='Ballet',
            choreographer='Sophia Williams',
            registration_fee=3500.00,
            description="""Ballet is a classical dance form demanding grace, precision, and strength. 
            Originating in the Italian Renaissance courts, ballet has evolved to become one of the most technical and beautiful art forms. 
            Our ballet classes focus on proper technique, alignment, and discipline. 
            Students will learn ballet terminology, positions, and movements while improving posture, flexibility, and core strength. 
            This class provides a strong foundation for all other dance styles."""
        )
        
        # Kathak
        kathak = DanceStyle.objects.create(
            name='Kathak',
            choreographer='Deepa Sharma',
            registration_fee=2800.00,
            description="""Kathak is one of the eight major forms of Indian classical dance, originating from North India. 
            The name Kathak is derived from the Sanskrit word katha meaning "story," and kathaka meaning "storyteller." 
            Our classes focus on rhythmic footwork, graceful pirouettes, and expressive storytelling through gestures (mudras) and facial expressions (abhinaya). 
            Students will learn to combine precise footwork with intricate rhythms created by ankle bells (ghungroo), while telling stories through movement."""
        )
        
        # Bharatanatyam
        bharatanatyam = DanceStyle.objects.create(
            name='Bharatanatyam',
            choreographer='Priya Patel',
            registration_fee=3200.00,
            description="""Bharatanatyam is one of the oldest classical dance forms of India, originating in Tamil Nadu. 
            This ancient art form is known for its grace, purity, tenderness, and sculpturesque poses. 
            Our classes focus on adavus (basic steps), mudras (hand gestures), expressions (abhinaya), and complex footwork. 
            Students will learn traditional items from the bharatanatyam repertoire while developing strong technique and storytelling abilities. 
            This dance style helps build discipline, concentration, and a deep connection to Indian culture."""
        )
        
        # Salsa
        salsa = DanceStyle.objects.create(
            name='Salsa',
            choreographer='Carlos Rodriguez',
            registration_fee=2500.00,
            description="""Salsa is a popular form of social dance that originated in the Caribbean, with strong influences from Latin America and Africa. 
            Our salsa classes teach the fundamentals of timing, partner connection, leading and following, and turn patterns. 
            Students will learn various salsa styles (Cuban, LA, NY) and develop confidence in social dancing. 
            This energetic dance style is perfect for those looking to improve coordination while having fun in a social environment. 
            No partner is necessary - we rotate partners throughout the class."""
        )
        
        # Add class slots
        self.stdout.write('Creating class slots...')
        
        # Class slots for Hip Hop
        ClassSlot.objects.create(
            dance_style=hip_hop,
            day='Monday',
            start_time=datetime.strptime('18:00', '%H:%M').time(),
            end_time=datetime.strptime('19:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=hip_hop,
            day='Thursday',
            start_time=datetime.strptime('19:00', '%H:%M').time(),
            end_time=datetime.strptime('20:30', '%H:%M').time()
        )
        
        # Class slots for Contemporary
        ClassSlot.objects.create(
            dance_style=contemporary,
            day='Tuesday',
            start_time=datetime.strptime('17:00', '%H:%M').time(),
            end_time=datetime.strptime('18:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=contemporary,
            day='Friday',
            start_time=datetime.strptime('18:00', '%H:%M').time(),
            end_time=datetime.strptime('19:30', '%H:%M').time()
        )
        
        # Class slots for Ballet
        ClassSlot.objects.create(
            dance_style=ballet,
            day='Monday',
            start_time=datetime.strptime('16:00', '%H:%M').time(),
            end_time=datetime.strptime('17:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=ballet,
            day='Wednesday',
            start_time=datetime.strptime('17:00', '%H:%M').time(),
            end_time=datetime.strptime('18:30', '%H:%M').time()
        )
        
        # Class slots for Kathak
        ClassSlot.objects.create(
            dance_style=kathak,
            day='Tuesday',
            start_time=datetime.strptime('19:00', '%H:%M').time(),
            end_time=datetime.strptime('20:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=kathak,
            day='Saturday',
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            end_time=datetime.strptime('11:30', '%H:%M').time()
        )
        
        # Class slots for Bharatanatyam
        ClassSlot.objects.create(
            dance_style=bharatanatyam,
            day='Wednesday',
            start_time=datetime.strptime('19:00', '%H:%M').time(),
            end_time=datetime.strptime('20:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=bharatanatyam,
            day='Saturday',
            start_time=datetime.strptime('16:00', '%H:%M').time(),
            end_time=datetime.strptime('17:30', '%H:%M').time()
        )
        
        # Class slots for Salsa
        ClassSlot.objects.create(
            dance_style=salsa,
            day='Thursday',
            start_time=datetime.strptime('17:00', '%H:%M').time(),
            end_time=datetime.strptime('18:30', '%H:%M').time()
        )
        ClassSlot.objects.create(
            dance_style=salsa,
            day='Sunday',
            start_time=datetime.strptime('18:00', '%H:%M').time(),
            end_time=datetime.strptime('19:30', '%H:%M').time()
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
