from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from dance_styles.models import DanceStyle as DanceStyleInfo # Renaming to avoid conflict if chatbot app had its own DanceStyle model

def chat_view(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
@login_required
def chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if not message:
                return JsonResponse({'message': 'Please enter a message'}, status=400)

            # Get response from the chatbot
            response = get_chatbot_response(message)
            
            return JsonResponse({'message': response})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'An error occurred'}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_chatbot_response(question):
    # Dance-specific response handler
    question_lower = question.lower()

    # --- Try to handle specific questions about Dance Styles --- 
    # Attempt to extract a known dance style name from the question
    all_dance_styles = DanceStyleInfo.objects.all()
    mentioned_style = None
    style_object = None

    for ds in all_dance_styles:
        if ds.name.lower() in question_lower:
            mentioned_style = ds.name
            style_object = ds
            break

    if style_object:
        if 'fee' in question_lower or 'cost' in question_lower or 'price' in question_lower:
            return f"<p>The registration fee for {style_object.name} is ${style_object.registration_fee}.</p>"
        elif 'choreographer' in question_lower or 'who teaches' in question_lower or 'instructor for' in question_lower:
            return f"<p>{style_object.choreographer} is the choreographer for {style_object.name}.</p>"
        elif 'tell me about' in question_lower or 'what is' in question_lower and style_object.name.lower() in question_lower or 'description of' in question_lower:
            response_html = f"<p><strong>{style_object.name}</strong></p>"
            if style_object.image:
                response_html += f"<img src='{style_object.image.url}' alt='{style_object.name}' style='max-width: 200px; height: auto; margin-bottom: 10px;'><br>"
            response_html += f"<p>Choreographer: {style_object.choreographer}</p>"
            response_html += f"<p>Registration Fee: ${style_object.registration_fee}</p>"
            response_html += f"<p>Description: {style_object.description}</p>"
            # We can add class slot info here later
            return response_html
        # Add more specific checks for style_object here if needed

    # --- Fallback to existing general responses ---
    question = question_lower # Use the lowercased question for the rest of the keyword checks

    dance_keywords = [
        'dance', 'dancer', 'dancing', 'ballet', 'hip-hop', 'salsa', 'contemporary',
        'tap', 'jazz', 'swing', 'ballroom', 'tango', 'flamenco', 'bharatanatyam',
        'kathak', 'breaking', 'locking', 'popping', 'technique', 'style', 'workshop',
        'class', 'lesson', 'practice', 'movement', 'rhythm', 'choreography',
        'performance', 'competition', 'audition', 'rehearsal', 'studio', 'teacher',
        'instructor', 'student', 'training', 'routine', 'exercise', 'stretch',
        'flexibility', 'strength', 'balance', 'coordination', 'expression',
        'costume', 'attire', 'shoes', 'outfit', 'clothing', 'wear', 'studio',
        'event', 'show', 'recital', 'competition', 'festival', 'exhibition'
    ]
    
    # Check if question is dance-related
    if not any(keyword in question for keyword in dance_keywords):
        return """<p>I'm here to help with dance-related questions! I can assist with:</p>
        <ul>
            <li>Specific dance styles and techniques</li>
            <li>Workshops and classes</li>
            <li>Equipment and clothing</li>
            <li>Training and practice</li>
            <li>Performance and events</li>
        </ul>
        <p>Try asking about something dance-related!</p>"""
    
    # Clothing and gear recommendations
    if any(word in question for word in ['wear', 'clothes', 'outfit', 'gear', 'attire', 'dress']):
        # Check for specific dance style
        if 'ballet' in question:
            return """<p>For ballet class, here's what you'll need:</p>
            <ul>
                <li>Leotard (any color)</li>
                <li>Tights (usually pink or black)</li>
                <li>Ballet slippers (pink or black)</li>
                <li>Hair in a neat bun or ponytail</li>
                <li>Optional: Leg warmers and arm warmers</li>
            </ul>
            <p>For men:</p>
            <ul>
                <li>White t-shirt</li>
                <li>Black tights or dance pants</li>
                <li>Ballet shoes</li>
                <li>Optional: Dance belt</li>
            </ul>
            <p>Tips for ballet attire:</p>
            <ul>
                <li>Choose comfortable, breathable fabrics</li>
                <li>Make sure your shoes fit properly</li>
                <li>Keep hair neat and out of your face</li>
                <li>Wear layers for temperature changes</li>
            </ul>
            <p>Would you like more specific tips about ballet attire or help with shoe fitting?</p>"""
        
        elif 'hip-hop' in question:
            return """<p>For hip-hop class, wear comfortable, casual clothing:</p>
            <ul>
                <li>Comfortable t-shirt or tank top</li>
                <li>Loose-fitting pants (sweatpants or joggers)</li>
                <li>Sneakers (clean, non-marking soles)</li>
                <li>Optional: Headband or bandana</li>
            </ul>
            <p>Tips for hip-hop attire:</p>
            <ul>
                <li>Choose clothing that allows full range of motion</li>
                <li>Wear shoes with good grip for floor work</li>
                <li>Stay comfortable but stylish</li>
                <li>Consider breathable fabrics for intense movement</li>
            </ul>
            <p>Would you like tips on specific hip-hop moves or choosing the right shoes?</p>"""
        
        elif 'salsa' in question:
            return """<p>For salsa class, here's what to wear:</p>
            <ul>
                <li>Comfortable, breathable top</li>
                <li>Loose-fitting pants or skirt</li>
                <li>Dance shoes with suede soles (or clean sneakers)</li>
                <li>Optional: Dance belt or garter</li>
            </ul>
            <p>Tips for salsa attire:</p>
            <ul>
                <li>Choose clothing that allows for quick turns and spins</li>
                <li>Wear shoes that provide good support and grip</li>
                <li>Avoid clothing that might get caught during partner work</li>
                <li>Consider wearing a skirt that allows for freedom of movement</li>
            </ul>
            <p>Would you like tips on salsa technique or partner work?</p>"""
        
        elif 'contemporary' in question:
            return """<p>For contemporary dance class, wear:</p>
            <ul>
                <li>Comfortable, stretchy clothing (leggings, yoga pants)</li>
                <li>Form-fitting top (tank top or t-shirt)</li>
                <li>Barefoot or in dance socks</li>
                <li>Optional: Dance shorts or leotard</li>
            </ul>
            <p>Tips for contemporary attire:</p>
            <ul>
                <li>Choose clothing that lets instructors see your alignment</li>
                <li>Wear something that allows for maximum range of motion</li>
                <li>Consider wearing layers for temperature changes</li>
                <li>Choose fabrics that wick away sweat</li>
            </ul>
            <p>Would you like tips on contemporary technique or floor work?</p>"""
        
        else:
            return """<p>For dance workshops, here's what to wear:</p>
            <ul>
                <li>Comfortable, stretchy clothing</li>
                <li>Layered clothing for temperature changes</li>
                <li>Appropriate dance shoes for your style</li>
                <li>Lightweight, breathable fabrics</li>
                <li>Nothing that restricts movement</li>
            </ul>
            <p>Which dance style are you interested in? I can provide more specific recommendations!</p>"""

    # History questions
    if any(word in question for word in ['history', 'origin', 'evolution']):
        response = """<p>Dance has a rich history dating back thousands of years. It evolved from ancient rituals and ceremonies to become an art form. Different cultures have their own unique dance traditions that reflect their history and values.</p>
        <p>For example:</p>
        <ul>
            <li>Ballet originated in the Italian Renaissance courts of the 15th century</li>
            <li>Hip-hop emerged in the African American communities of New York City in the 1970s</li>
        </ul>
        <p>Would you like to learn more about a specific dance style's history?</p>"""
        return response
    
    # Styles questions
    if any(word in question for word in ['styles', 'types', 'genres']):
        response = """<p>There are many dance styles including:</p>
        <ul>
            <li>Traditional styles: Ballet, Tap, Jazz, Modern</li>
            <li>Social dances: Salsa, Swing, Ballroom, Tango</li>
            <li>Street dances: Hip-hop, Breaking, Popping, Locking</li>
            <li>Cultural dances: Bharatanatyam, Kathak, Flamenco, Irish Step Dance</li>
            <li>Contemporary styles: Contemporary, Lyrical, Musical Theatre</li>
        </ul>
        <p>Which style interests you the most? I can provide more details about its techniques and origins.</p>"""
        return response
    
    # Technique questions
    if any(word in question for word in ['technique', 'training', 'practice', 'how to']):
        response = """<p>Dance training involves several key aspects:</p>
        <ul>
            <li>Basic technique: Proper posture, alignment, and movement fundamentals</li>
            <li>Strength and flexibility: Regular stretching and conditioning exercises</li>
            <li>Rhythm and timing: Learning to move in sync with music</li>
            <li>Expression: Developing emotional connection and performance quality</li>
            <li>Repertoire: Learning and practicing various dance combinations</li>
        </ul>
        <p>Which aspect would you like to focus on? I can provide specific exercises and tips for improvement.</p>"""
        return response
    
    # Benefits questions
    if any(word in question for word in ['benefits', 'advantages', 'good for']):
        response = """<p>Dancing offers numerous benefits:</p>
        <ul>
            <li>Physical benefits:
                <ul>
                    <li>Improved cardiovascular health</li>
                    <li>Increased flexibility and strength</li>
                    <li>Better coordination and balance</li>
                    <li>Weight management</li>
                </ul>
            </li>
            <li>Mental benefits:
                <ul>
                    <li>Stress relief</li>
                    <li>Improved mood</li>
                    <li>Enhanced confidence</li>
                    <li>Better cognitive function</li>
                </ul>
            </li>
            <li>Social benefits:
                <ul>
                    <li>Meeting new people</li>
                    <li>Building teamwork</li>
                    <li>Cultural appreciation</li>
                    <li>Creative expression</li>
                </ul>
            </li>
        </ul>
        <p>Which aspect interests you most? I can provide personalized recommendations based on your goals.</p>"""
        return response
    
    # Beginner questions
    if any(word in question for word in ['beginner', 'start', 'begin', 'new to']):
        response = """<p>Starting dance is exciting! Here are some tips:</p>
        <ul>
            <li>Choose a style that interests you</li>
            <li>Find beginner classes in your area</li>
            <li>Start with basic movements</li>
            <li>Practice regularly</li>
            <li>Have fun and be patient with yourself</li>
        </ul>
        <p>What style are you interested in? I can help you find beginner classes and resources.</p>"""
        return response
    
    # Vague input handling
    if len(question.split()) < 3:
        return """<p>I see you're interested in dance! To help you better, could you please:</p>
        <ul>
            <li>Ask about a specific dance style</li>
            <li>Tell me your experience level</li>
            <li>Share what you'd like to learn</li>
        </ul>
        <p>For example: 'What's the history of ballet?' or 'How can I improve my hip-hop technique?'</p>"""
    
    # General question handling
    return """<p>I'm here to help! How can I assist you with dance?</p>
        <ul>
            <li>Learn about different dance styles</li>
            <li>Get training tips</li>
            <li>Understand dance history</li>
            <li>Find local classes</li>
            <li>Get clothing recommendations</li>
        </ul>
        <p>Just let me know what you'd like to know more about!</p>"""
        # return """<p>Starting dance is exciting! Here are some tips:</p>
        # <ol>
        #     <li>Choose a style you're interested in</li>
        #     <li>Find a beginner class or online tutorial</li>
        #     <li>Wear comfortable, flexible clothing</li>
        #     <li>Start with basic steps and build gradually</li>
        #     <li>Don't be afraid to make mistakes - they're part of learning</li>
        #     <li>Practice regularly, even if it's just a few minutes a day</li>
        #     <li>Have fun and enjoy the journey!</li>
        # </ol>
        # <p>Remember, everyone starts as a beginner, and progress comes with consistent practice.</p>"""
    
    # Performance questions
    if any(word in question for word in ['performance', 'stage', 'show']):
        return """<p>For successful dance performances:</p>
        <ol>
            <li>Practice consistently until movements become second nature</li>
            <li>Focus on expression and storytelling</li>
            <li>Work on stage presence and confidence</li>
            <li>Practice with the music you'll perform to</li>
            <li>Visualize your performance before going on stage</li>
            <li>Stay hydrated and warmed up before performing</li>
            <li>Remember to breathe and enjoy the moment!</li>
        </ol>"""
    
    # Competition questions
    if any(word in question for word in ['competition', 'contest', 'competition']):
        return """<p>For dance competitions:</p>
        <ol>
            <li>Choose a routine that suits your strengths</li>
            <li>Practice your routine until it's flawless</li>
            <li>Pay attention to technique and execution</li>
            <li>Work on your stage presence and performance quality</li>
            <li>Follow all competition rules and guidelines</li>
            <li>Stay calm and focused during performance</li>
            <li>Learn from feedback and use it to improve</li>
        </ol>"""
    
    # Default response
    return """<p>I'm here to help with dance-related questions! You can ask about:</p>
        <ul>
            <li>Dance history and origins</li>
            <li>Different dance styles</li>
            <li>Training techniques</li>
            <li>Benefits of dancing</li>
            <li>Getting started as a beginner</li>
            <li>Performance tips</li>
            <li>Competition preparation</li>
        </ul>
        <p>What would you like to know more about?</p>"""

@login_required
def chat_view(request):
    return render(request, 'chatbot/chat.html')
