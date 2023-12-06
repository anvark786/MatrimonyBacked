from rest_framework import viewsets
from .serializers import SocialMediaSerializer,SocialLinkAccessRequestSerializer
from .models import SocialMedia,SocialLinkAccessRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import datetime



class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer    
    permission_classes = [IsAuthenticated]
    


class SocialLinkAccessRequestViewSet(viewsets.ModelViewSet):
    queryset = SocialLinkAccessRequest.objects.all()
    serializer_class = SocialLinkAccessRequestSerializer    
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['PATCH'])
    def accept_access_request(self, request, pk=None):
        access_request = self.get_object()
        if access_request.status !="pending":
            response_data = {
            'StatusCode':6001,
            'message':"Already Made an Action!."
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        access_request.status = "approved"
        access_request.updated_at = datetime.now()
        access_request.save()
        response_data = {
            'StatusCode':6000,
            'message':"Successfully Approved."
            }
        return Response(response_data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['PATCH'])
    def decline_access_request(self, request, pk=None):
        access_request = self.get_object()
        if access_request.status !="pending":
            response_data = {
            'StatusCode':6001,
            'message':"Already Made an Action!."
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        access_request.status = "declined"
        access_request.updated_at = datetime.now()
        access_request.save()
        response_data = {
            'StatusCode':6000,
            'message':"Successfully Declined!."
            }
        return Response(response_data, status=status.HTTP_200_OK)