from rest_framework import serializers
from .models import Profile,Address,Occupation,FamilyDetails,Education, ProfilePhotoViewRequest,Religion,Community,Preference,Photo,ProfileInterest
from users.serializers import UserSerializer
from social_meadia.models import SocialMedia,SocialLinkAccessRequest
from social_meadia.serializers import SocialMediaSerializer 

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
    partner_preference = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()

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
        account_plan = getattr(request.user.profile, "account_plan", None)
        if not account_plan or account_plan.code == "free":
            return None
        address = Address.objects.filter(profile=obj).first()
        if address:
            serializer =  AddressSerializer(address,many=False,context={"request":request})
            user_mobile = obj.user.phone_number
            user_email = obj.user.email            
            return {**serializer.data, 'phone_number':user_mobile,'email':user_email}
        return None
        
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
        
    def get_partner_preference(self,obj):
        request = self.context.get("request") 
        partner_preference = Preference.objects.filter(profile=obj).first()
        if partner_preference:
            serializer =  PreferenceSerializer(partner_preference,many=False,context={"request":request})
            return serializer.data
        
    def get_photos(self,obj):
        photos = Photo.objects.filter(profile=obj)
        request = self.context.get("request") 
        if photos:
            photo_serialaizer = PhotoSerializer(photos,many=True,context={"request":request})
            return photo_serialaizer.data
        
    def get_social_links(self,obj):
        social_links =  SocialMedia.objects.filter(owner=obj.user)
        request = self.context.get("request") 
        account_plan = getattr(request.user.profile, "account_plan", None)
        if not request.user.is_authenticated or not account_plan or account_plan.code == 'free':
            return []
        if obj.is_locked_social_accounts and not(
            SocialLinkAccessRequest.objects.filter(
                requester__user=request.user,
                profile_owner__user=obj.user,
                status="approved"
                ).exists()) and request.user != obj.user:
            return []
        if social_links:
            social_links_serialaizer = SocialMediaSerializer(social_links,many=True,context={"request":request})
            return social_links_serialaizer.data
        
class ProfileListSmallSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    religion = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude =['deleted','deleted_by_cascade','created_by','updated_by']


    def get_name(self,obj):
        name = str(obj.user.first_name)+" "+str(obj.user.last_name)
        return name
    
    def get_profession(self,obj):
        occupation = Occupation.objects.filter(profile=obj).first()
        if occupation:
            occupation = occupation.profession
        return occupation

    def get_education(self,obj):
        education = Education.objects.filter(profile=obj).first()
        if education:
            education = education.get_name_display()
        return education

    def get_religion(self,obj):
        religion =None
        if obj.community:
            religion = obj.community.religion.name       
        return religion
    
    def get_location(self,obj):
        location = None
        address = Address.objects.filter(profile=obj).first()
        if address:
            location = address.city
        return location
         
    def get_profile_pic(self,obj):
        photo = Photo.objects.filter(profile=obj).first()
        request = self.context.get("request")
        if photo:
            photo_serialaizer = PhotoSerializer(photo,many=False,context={"request":request})
            return photo_serialaizer.data

    
        
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class ProfileInterestSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    sender_data = serializers.SerializerMethodField(read_only=True)
    receiver_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProfileInterest
        fields = '__all__'

    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        
        return data
    
    def get_sender_data(self,obj):
        return {
            'id': obj.sender.id,
            'profile_id': obj.sender.profile_id,
            'name': obj.sender.user.first_name + " " + obj.sender.user.last_name
        }
    
    def get_receiver_data(self,obj):
        return {
            'id': obj.receiver.id,
            'profile_id': obj.receiver.profile_id,
            'name': obj.receiver.user.first_name + " " + obj.receiver.user.last_name,
        }


class ProfilePhotoViewRequestSerializer(serializers.ModelSerializer):
    
    sender = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    class Meta:
        model = ProfilePhotoViewRequest
        fields = '__all__'

    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        
        if ProfilePhotoViewRequest.objects.filter(sender=sender, receiver=receiver, status='pending').exists():
            raise serializers.ValidationError("A pending request already exists between these users.")        
        return data
    
    def get_sender_data(self,obj):
        return {
            'id': obj.sender.id,
            'profile_id': obj.sender.profile_id,
            'name': obj.sender.user.first_name + " " + obj.sender.user.last_name
        }

    def get_receiver_data(self,obj):
        return {
            'id': obj.receiver.id,
            'profile_id': obj.receiver.profile_id,
            'name': obj.receiver.user.first_name + " " + obj.receiver.user.last_name
        }
    