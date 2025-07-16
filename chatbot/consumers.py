import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import views

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message'].strip()

            if not message:
                await self.send(text_data=json.dumps({
                    'message': 'Please ask a question about dance!'
                }))
                return

            # Simple response system
            response = self.get_dance_response(message)
            
            await self.send(text_data=json.dumps({
                'message': response
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'message': 'Invalid message format. Please try again.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': 'Sorry, I encountered an error. Please try again later.'
            }))

    def get_dance_response(self, question):
        # Simple dance-related responses
        question = question.lower()
        
        if 'history' in question or 'origin' in question:
            return "Dance has ancient origins dating back to prehistoric times, used in rituals, celebrations, and storytelling across cultures."
        
        if 'styles' in question or 'types' in question:
            return "There are many dance styles including ballet, hip-hop, contemporary, salsa, ballroom, and traditional dances from various cultures."
        
        if 'technique' in question or 'training' in question:
            return "Dance training involves learning proper posture, alignment, flexibility, strength, and rhythm. It's important to practice regularly and focus on technique."
        
        if 'benefits' in question:
            return "Dancing offers many benefits including improved physical fitness, mental health, social skills, and artistic expression. It's great for all ages!"

class DanceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message'].strip()

            if not message:
                await self.send(text_data=json.dumps({
                    'message': 'Please ask a dance-related question!'
                }))
                return

            # Get response using the enhanced dance chatbot
            response = views.get_chatbot_response(message)
            
            await self.send(text_data=json.dumps({
                'message': response
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'message': 'Invalid message format. Please try again.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': 'Sorry, I encountered an error. Please try again later.'
            }))
        
        if 'beginner' in question or 'start' in question:
            return "To start dancing, choose a style you like, find a beginner class, wear comfortable clothing, and most importantly, have fun!"
        
        # Default response
        return "I'm here to help with dance-related questions! Ask about history, styles, techniques, or any other dance topic."

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'message': message
        }))
