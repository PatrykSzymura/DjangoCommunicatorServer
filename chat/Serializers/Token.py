
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from chat import models as m

# Token Serializers
class DuckToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        requested_chatUser_data = m.ChatUser.objects.get(user=user)

        token['authority'] = requested_chatUser_data.authorityLevel

        return token