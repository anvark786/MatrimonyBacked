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


    def create(self, request, *args, **kwargs):
        requester = request.data.get('requester',None)
        profile_owner = request.data.get('profile_owner',None)
        if requester==profile_owner:
           return Response({'error': 'Requester and profile owner cannot be the same person.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(detail=True, methods=['PATCH'])
    def handle_social_request(self, request, pk=None):
        action_type = request.data.get('action',None)
        access_request = self.get_object()
        if access_request.status !="pending":
            response_data = {
            'StatusCode':6001,
            'message':"Already Made an Action!."
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        if action_type == "accept":
            access_request.status = "approved"
            access_request.updated_at = datetime.now()
            access_request.save()
            response_data = {
                'StatusCode':6000,
                'message':"Successfully Approved."
                }
            return Response(response_data, status=status.HTTP_200_OK)
        elif action_type == "reject":
            access_request.status = "declined"
            access_request.updated_at = datetime.now()
            access_request.save()
            response_data = {
                'StatusCode':6000,
                'message':"Successfully Declined!."
                }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data = {'StatusCode':6001,'message':"Somthing wrong!."}, status=status.HTTP_406_NOT_ACCEPTABLE)

