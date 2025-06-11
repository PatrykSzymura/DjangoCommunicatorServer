from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from chat import models as m

# Custom token serializer that extends the default JWT token response
class DuckToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Call the base method to generate the standard token
        token = super().get_token(user)

        # Add custom user data to the token payload
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Fetch related ChatUser instance to include authority level
        requested_chatUser_data = m.ChatUser.objects.get(user=user)
        token['authority'] = requested_chatUser_data.authorityLevel

        return token