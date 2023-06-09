from rest_framework import serializers, status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from . models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password','full_name','username')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            username=validated_data['username']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type':'password'})
    
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        email = data['email']
        password = data['password']

        if not email:
            raise serializers.ValidationError('Email is required')
        if not password:
            raise serializers.ValidationError('Password is required')
        
        user = authenticate(request=self.request, email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        return user
    
class ShowDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UpdateInformationOfUserSerializer(serializers.ModelSerializer):
    follower_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = '__all__'

        def update(self, instance, validated_data):
            instance.profile_picture = validated_data.get('picture', instance.profile_picture)
            instance.full_name = validated_data.get('full_name', instance.full_name)
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.is_private_account = validated_data.get('is_private_account', instance.is_private_account)
            instance.website = validated_data.get('website', instance.website)
            instance.save()
            return instance
        
        

class USerProfileSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','bio','profile_picture','full_name','website', 'is_private_account')