
from rest_framework import viewsets
from .models import Profile,Preference,Religion,Community,Education,Occupation,FamilyDetails,Address
from .serializers import ProfileSerializer,ReligionSerializer,CommunitySerializer,EducationSerializer,OccupationSerializer,FamilyDetailsSerializer,AddressSerializer,PreferenceSerializer
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
            serializer = ProfileSerializer(profiles,many=True,context={"request":request})
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