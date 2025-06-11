from rest_framework import serializers
from chat import models as m

# Returns Channel
# ID & NAME
class BriefChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Channel
        fields = ['id', 'name']

# Returns Channel
# ID & NAME & DESCRIPTION
class DetailChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Channel
        fields = ['id','name','description']
        extra_kwargs = {'description': {'required': False},'id': {'read_only': True}}


