from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email']
        
class ProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email','role']

class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    set_password_code = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    
class UpdateProfileRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    ph_no = serializers.CharField(required=False)

class UpdateProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'ph_no', 'role']