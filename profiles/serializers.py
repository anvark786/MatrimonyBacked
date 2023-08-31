from rest_framework import serializers
from .models import Profile,Address,Occupation,FamilyDetails,Education,Religion,Community,Preference
from users.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class FamilyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =FamilyDetails
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'

class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = '__all__'
       
    
class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    religous_data = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    family_details = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_user_data(self,obj):
        request = self.context.get("request") 
        user = obj.user
        serializer =  UserSerializer(user,many=False,context={"request":request})
        return serializer.data
    
    def get_address(self,obj):
        request = self.context.get("request") 
        address = Address.objects.filter(profile=obj).first()
        if address:
            serializer =  AddressSerializer(address,many=False,context={"request":request})
            return serializer.data
        
    def get_occupation(self,obj):
        request = self.context.get("request") 
        occupation = Occupation.objects.filter(profile=obj).first()
        if occupation:
            serializer =  OccupationSerializer(occupation,many=False,context={"request":request})
            return serializer.data
        
    def get_family_details(self,obj):
        request = self.context.get("request") 
        family_details = FamilyDetails.objects.filter(profile=obj).first()
        if family_details:
            serializer =  FamilyDetailsSerializer(family_details,many=False,context={"request":request})
            return serializer.data
        
    def get_education(self,obj):
        request = self.context.get("request") 
        education = Education.objects.filter(profile=obj)
        if education:
            serializer =  EducationSerializer(education,many=True,context={"request":request})
            return serializer.data
        
    def get_religous_data(self,obj): 
        if obj.community:
            religion = obj.community.religion.name
            religous_data = {
                'religion':religion,
                'sector':obj.community.name
            }
            return religous_data
        

class ProfileListSmallSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    religion = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields ='__all__'


    def get_name(self,obj):
        name = str(obj.user.first_name)+" "+str(obj.user.last_name)
        return name
    
    def get_profession(self,obj):
        profession = Occupation.objects.filter(profile=obj).first().profession
        return profession

    def get_education(self,obj):
        education = Education.objects.filter(profile=obj).first().name
        return education

    def get_religion(self,obj):
        religion = Religion.objects.filter(profile=obj).first().name
        return religion
    
    def get_location(self,obj):
        address = Address.objects.filter(profile=obj).first()
        location = str(address.street)+","+str(address.location)+","+str(address.district)
        return location
         

       