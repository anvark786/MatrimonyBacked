from rest_framework import viewsets
from .serializers import SocialMediaSerializer,SocialLinkAccessRequestSerializer
from .models import SocialMedia,SocialLinkAccessRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status



class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer    
    permission_classes = [IsAuthenticated]


class SocialLinkAccessRequestViewSet(viewsets.ModelViewSet):
    queryset = SocialLinkAccessRequest.objects.all()
    serializer_class = SocialLinkAccessRequestSerializer    
    permission_classes = [IsAuthenticated]