from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . serializer import SignupSerializer, LoginSerializer, ShowDataSerializer, UpdateInformationOfUserSerializer, USerProfileSearchSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from .models import User
from datetime import timedelta, datetime
from django.db.models import Q

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(request=request,data=request.data)
        print(request,request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request=request, user=user)
            response = Response()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data['refresh_token']
        if refresh_token:
            try:
                access_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
                access_token_obj = AccessToken(access_token)
                access_token_obj.set_exp(lifetime=timedelta(seconds=10))
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.blacklist()
                logout(request=request)
                return Response({"msg":"Token Blacklisted"},status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class UserInformationUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            user = request.user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateInformationOfUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_object = User.objects.all()
        serializer = ShowDataSerializer(user_object, many=True)
        return Response(serializer.data)
    
class SearchAllProfiles(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        search_term = kwargs.get('search_term',None)
        if search_term:
            print(request.user.username, type(request.user.username))
            search_profiles = User.objects.filter(
                Q(username__icontains = str(search_term)) | Q(full_name__contains = search_term)
                & Q(is_active=True)
                ).exclude(username=request.user.username)
            serializer = USerProfileSearchSerializer(search_profiles, many=True, context={'request': request})
            context = {'search_profiles':serializer.data}
            print(search_profiles)
            return Response(data=context, status=status.HTTP_302_FOUND)
        search_profiles = User.objects.none()    
        context = {'search_profiles':search_profiles}
        return Response(data=context, status=status.HTTP_204_NO_CONTENT)