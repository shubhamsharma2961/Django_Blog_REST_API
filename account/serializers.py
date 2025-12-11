from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'middle_name', 'address', 'number', 'email', 'date_of_birth', 'age', 'gender']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField()
    number = serializers.CharField()
    date_of_birth = serializers.DateField()
    age = serializers.IntegerField()
    gender = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already taken')
        if UserProfile.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already in use')
        return data

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password']
        }
        user = User.objects.create_user(**user_data)
        profile_data = {
            'user': user,
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'middle_name': validated_data.get('middle_name', ''),
            'address': validated_data['address'],
            'number': validated_data['number'],
            'email': validated_data['email'],
            'date_of_birth': validated_data['date_of_birth'],
            'age': validated_data['age'],
            'gender': validated_data['gender']
        }
        UserProfile.objects.create(**profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account not found')
        return data

    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return {'message': 'Invalid credentials', 'data': ''}
        
        refresh = RefreshToken.for_user(user)
        return {
            'message': 'Login success',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        }
"""
class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('username already taken') 
        return data
    
    def create(self, validated_data):
        user= User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'].lower()
        )
        user.set_password(validated_data['password']) 
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    # password = serializers.CharField(write_only=True)
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('account not found') 
        return data

    def get_jwt_token(self, data):
        user = authenticate(username = data['username'], password = data['password'])
        
        if not user:
            return{'message':'invalid credentials', 'data':''}
        
        refresh = RefreshToken.for_user(user)

        return{'message':'login success', 'data': {'token' :{ 'refresh': str(refresh),'access': str(refresh.access_token)}}}



"""   

        