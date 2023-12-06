from rest_framework import serializers
from .models import SocialLinkAccessRequest,SocialMedia



class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class SocialLinkAccessRequestSerializer(serializers.ModelSerializer):
    profile_requester_name = serializers.SerializerMethodField() 
    status_display = serializers.CharField(source='get_status_display',read_only=True)
    profile_requester_uuid = serializers.SerializerMethodField() 

    class Meta:
        model = SocialLinkAccessRequest
        exclude = ['deleted','deleted_by_cascade','created_by','updated_by']

    def get_profile_requester_name(self,obj):
        name = str(obj.requester.user.first_name)+" "+str(obj.requester.user.last_name)+"("+str(obj.requester.profile_id)+")"
        return name
    
    def get_profile_requester_uuid(self,obj):
        uuid = obj.requester.uuid
        return uuid