
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
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from matrimony.utils import send_nms_sms,generate_otp_with_otpms,verify_otp_with_otpms

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'age': ['lte', 'gte'],
        'height': ['lte', 'gte'],
        'weight': ['lte', 'gte'],
        'complexion': ['exact', 'in'],
        'blood_group': ['exact'],
        'community__name': ['exact', 'in'],
        'marital_status': ['exact'],
        'physical_status': ['exact'],
        'is_locked_photos': ['exact'],
        'is_locked_social_accounts': ['exact'],
        'educations__name': ['exact'],
        'occupation__profession_type': ['exact', 'in'],
        'address__district': ['exact'],
        'address__city': ['exact'],
        'address__location': ['exact'],
        'family__financial_status': ['exact', 'in'],
    }
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.query_params.get('basic', False):
            return ProfileListSmallSerializer
        else:           
            return ProfileSerializer
        
    def get_queryset(self):
        queryset = Profile.objects.all() 
        if not self.request.user.is_admin:
            user_profile = self.request.user.profile
            user_gender = user_profile.user.gender
            
            if self.action == 'list':
                queryset = queryset.exclude(user=user_profile.user)                
            excluded_profiles = Profile.objects.filter(Q(user__gender=user_gender) & ~Q(user=user_profile.user))
            queryset = queryset.exclude(id__in=excluded_profiles.values_list('id', flat=True))

        return queryset

    @action(detail=True, methods=['GET'])
    def matching_profiles(self, request, pk=None):
        profile = self.get_object()
        profiles = get_matching_profiles(profile.pk)
        paginated_results = self.paginate_queryset(profiles) 
        if paginated_results:          
            serializer = ProfileListSmallSerializer(paginated_results,many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)
        elif profiles:          
            serializer = ProfileListSmallSerializer(profiles,many=True,context={"request":request})
        return Response(serializer.data)  

    
    @action(detail=False, methods=['GET'],url_path='search-by-id')
    def search_by_profile_id(self, request, pk=None):
        profile_id = request.query_params.get('profile_id',None)
        gender_selection = 'M'
        if request.user.gender == 'M':
            gender_selection = 'F'       
        if profile_id:
            profile = Profile.objects.filter(profile_id=profile_id,user__gender=gender_selection)
            if profile:
                serializer = ProfileListSmallSerializer(profile,many=True,context={"request":request})
                return Response(serializer.data)   
            else:
                return Response([])  
        else:
            return Response({'error': 'Profile ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)  

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
    
    @action(detail=False, methods=['GET'])
    def check_social_request(self, request):
        uuid = request.query_params.get('uuid',None)
        print(request.user.profile,"request.user.profile")
        if uuid:
            request = SocialLinkAccessRequest.objects.filter(profile_owner__uuid=uuid,requester=request.user.profile).first()
        if request:
            serializer = SocialLinkAccessRequestSerializer(request,many=False,context={"request":request})
            return Response(serializer.data)        
        return Response({})
    
    @action(detail=True, methods=['GET'])
    def recived_social_request(self, request,pk=None):
        profile = self.get_object()
        requests = SocialLinkAccessRequest.objects.filter(profile_owner=profile)     
        paginated_results = self.paginate_queryset(requests) 
        if paginated_results:
            serializer = SocialLinkAccessRequestSerializer(paginated_results,many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)
        serializer = SocialLinkAccessRequestSerializer(requests,many=True,context={"request":request})
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def list_of_requests_send_by_profile(self, request,pk=None):
        profile = self.get_object()
        requests = SocialLinkAccessRequest.objects.filter(requester=profile)     
        paginated_results = self.paginate_queryset(requests) 
        if paginated_results:
            serializer = SocialLinkAccessRequestSerializer(paginated_results,many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)
        serializer = SocialLinkAccessRequestSerializer(requests,many=True,context={"request":request})
        return Response(serializer.data)
    
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