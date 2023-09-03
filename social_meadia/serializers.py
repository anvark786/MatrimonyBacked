from rest_framework import serializers
from .models import SocialLinkAccessRequest,SocialMedia



class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class SocialLinkAccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinkAccessRequest
        fields = '__all__'