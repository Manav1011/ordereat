from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from Profile.models import Profile
from Restaurant.models import Franchise, Outlet
from django.shortcuts import get_object_or_404
from Profile.serializers import (
    ProfileSerializer, 
    ProfileResponseSerializer, 
    SetPasswordSerializer,
    UpdateProfileRequestSerializer,
    UpdateProfileResponseSerializer,
)
from Restaurant.serializers import FranchiseSerializer, OutletSerializer
from ordereat.GlobalUtils import generate_unique_hash

class CreateFranchiseAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, franchise_slug):
        franchise = get_object_or_404(Franchise, slug=franchise_slug)
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)  # <-- Use serializer_class
        if serializer.is_valid():            
            profile = serializer.save()
            profile.role = 'franchise_owner'
            profile.save()
            franchise.admin = profile
            franchise.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOutletAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, outlet_slug):
        outlet = get_object_or_404(Outlet, slug=outlet_slug)
        if outlet.franchise.admin is None or outlet.franchise.admin != request.user:
            return Response({'detail': 'Only the restaurant admin can assign outlet admins.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)  # <-- Use serializer_class
        if serializer.is_valid():
            serializer.validated_data['role'] = 'outlet_owner'
            profile = serializer.save()
            profile.role = 'outlet_owner'
            profile.save()
            outlet.admin = profile
            outlet.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(APIView):
    """
    Set a new password using email and forgot_password_code.
    """    

    serializer_class = SetPasswordSerializer
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        code = serializer.validated_data['set_password_code']
        new_password = serializer.validated_data['new_password']
        user = get_object_or_404(Profile, email=email)
        if user.forgot_password_code != code:
            return Response({'detail': 'Invalid password reset code.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.forgot_password_code = generate_unique_hash()
        user.save()
        return Response({'detail': 'Password has been set successfully.'}, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = request_serializer_class = UpdateProfileRequestSerializer
    response_serializer_class = UpdateProfileResponseSerializer

    def put(self, request):
        user = request.user
        serializer = self.request_serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Only update provided fields
        for attr, value in serializer.validated_data.items():
            setattr(user, attr, value)
        user.save()
        response_serializer = self.response_serializer_class(user)
        return Response({
            'detail': 'Profile updated successfully.',
            'profile': response_serializer.data
        }, status=status.HTTP_200_OK)