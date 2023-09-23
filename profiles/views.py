
from rest_framework import viewsets
from .models import Profile,Preference,Religion,Community,Education,Occupation,FamilyDetails,Address,Photo
from social_meadia.models import SocialMedia,SocialLinkAccessRequest
from social_meadia.serializers import SocialMediaSerializer,SocialLinkAccessRequestSerializer
from .serializers import ProfileSerializer,ReligionSerializer,CommunitySerializer,EducationSerializer,OccupationSerializer,FamilyDetailsSerializer,AddressSerializer,PreferenceSerializer,PhotoSerializer,ProfileListSmallSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .functions import get_matching_profiles
from django.shortcuts import get_object_or_404
from rest_framework import status




class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def matching_profiles(self, request, pk=None):
        profile = self.get_object()
        profiles = get_matching_profiles(profile.pk)
        if profiles:          
            serializer = ProfileListSmallSerializer(profiles,many=True,context={"request":request})
            return Response(serializer.data)
        return Response(profiles)    

    @action(detail=False, methods=['GET'])
    def profile_by_uuid(self, request):
        uuid = request.query_params.get('uuid')
        if uuid:
            profile = get_object_or_404(Profile, uuid=uuid)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:
            return Response({'error': 'UUID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET'])
    def profile_photos(self, request,pk=None):
        profile = self.get_object()
        photos = []
        photos = Photo.objects.filter(profile=profile.pk)
        if photos:
            serializer = PhotoSerializer(photos,many=True,context={"request":request})
            return Response(serializer.data)
        return Response({'message': 'Profile Photos not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def social_accounts(self, request,pk=None):
        profile = self.get_object()
        is_locked_social = profile.is_locked_social_accounts
        social_accounts = SocialMedia.objects.filter(owner=profile.user)
        if social_accounts:
            serializer = SocialMediaSerializer(social_accounts,many=True,context={"request":request})
            return Response({"is_locked_social":is_locked_social,"data":serializer.data})
        return Response({'message': 'Social Accounts not found'}, status=status.HTTP_400_BAD_REQUEST)    
    
    @action(detail=True, methods=['GET'])
    def social_requests(self, request,pk=None):
        profile = self.get_object()
        request = SocialLinkAccessRequest.objects.filter(profile_owner=profile)
        if request:
            serializer = SocialLinkAccessRequestSerializer(request,many=True,context={"request":request})
            return Response(serializer.data)        
        return Response([])   

    @action(detail=True, methods=['PATCH'])
    def lock_or_unlock_social(self, request, pk=None):
        profile = self.get_object()
        profile.is_locked_social_accounts = not profile.is_locked_social_accounts
        profile.save()
        if profile.is_locked_social_accounts:
            message = 'Social Accounts Disabled successfully'
        else:
            message = 'Social Accounts Enabled successfully'
        return Response({'message': message}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def check_social_request(self, request,pk=None):
        profile = self.get_object()
        request = SocialLinkAccessRequest.objects.filter(requester=profile).first()
        if request:
            serializer = SocialLinkAccessRequestSerializer(request,many=False,context={"request":request})
            return Response(serializer.data)        
        return Response({})


class ReligionViewSet(viewsets.ModelViewSet):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer    
    permission_classes = [IsAuthenticated]

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer  
    permission_classes = [IsAuthenticated]

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer  
    permission_classes = [IsAuthenticated]

class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer  
    permission_classes = [IsAuthenticated]

class FamilyDetailsViewSet(viewsets.ModelViewSet):
    queryset = FamilyDetails.objects.all()
    serializer_class = FamilyDetailsSerializer  
    permission_classes = [IsAuthenticated]

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer  
    permission_classes = [IsAuthenticated]

class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer  
    permission_classes = [IsAuthenticated]

class PhotoiewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer  
    permission_classes = [IsAuthenticated]