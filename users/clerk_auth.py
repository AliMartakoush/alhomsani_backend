from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
#from clerk_sdk_python import Clerk
#from .models import NewUser

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Initialize Clerk client
            clerk = Clerk(secret_key=settings.CLERK_SECRET_KEY)
            
            # Extract the token from the Authorization header
            token = auth_header.split(' ')[1]
            
            # Verify the session token
            session = clerk.sessions.verify_token(token)
            
            # Get the user ID from the session
            user_id = session.user_id
            
            # Get or create the user
            user, created = NewUser.objects.get_or_create(
                clerk_id=user_id,
                defaults={
                    'email': session.user.email_addresses[0].email_address,
                    'username': session.user.username or session.user.email_addresses[0].email_address,
                }
            )
            
            return (user, None)
            
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid token') 