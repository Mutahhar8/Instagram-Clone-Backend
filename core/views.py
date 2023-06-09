from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.models import User
from django.shortcuts import get_object_or_404
from .models import Post, Follow, Like, Comment, SavedPost
from .serializer import PostSerializer, FollowSerializer, CommentsViewSerializer, CommentUpdateSerializer, SavedPostSerializer, NewFeedsPostSerializer
import uuid
from django.conf import settings
from django.contrib.auth import login, logout
from allauth.socialaccount.models import SocialAccount, SocialToken
import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from google.oauth2 import id_token
from django.contrib.auth import get_user_model
User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPostsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        posts = Post.objects.filter(user=request.user, is_active=True).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, pk):
        try:
            post = get_object_or_404(Post, pk=pk, user=request.user)
        except Exception as e:
            return Response({"error":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(instance=post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeletePostsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)        
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowDoneView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        followed_user_id = request.POST.get('followed_user_id')
        if followed_user_id == request.user:
            return Response({'error':'cannot follow yourself'},status=status.HTTP_400_BAD_REQUEST)
        followed_user_obj = User.objects.get(pk=followed_user_id)
        try:
            follow_obj = Follow.objects.get(user=request.user, followed=followed_user_obj)
            return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        except Follow.DoesNotExist:
            follow_obj = Follow.objects.create(user=request.user, followed=followed_user_obj)
            serializer = FollowSerializer(follow_obj)
            return Response(serializer.data)

class UnfollowDoneView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)
        try:
            unfollow_obj = Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            unfollow_obj.delete()
        except Follow.DoesNotExist:
            pass
        return Response({'msg':'unfollowed done!!'}, status=status.HTTP_200_OK)
    

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id is None:
            return Response({'error':'no post id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            like_obj = get_object_or_404(Like, user=request.user, post_id=post_id)
            like_obj.is_like = True
            like_obj.save()
        except Exception as e:
            Like.objects.create(user=request.user, post_id=post_id)
        return Response({'msg':'liked the post'},status=status.HTTP_201_CREATED)
        # return redirect(request.META.get('HTTP_REFERER'))
    

class PostUnLikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id is None:
            return Response({'error':'no post id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            like_object = get_object_or_404(Like, user=request.user, post_id=post_id)
            like_object.is_like = False
            like_object.save()
            return Response({'msg':'unliked the post'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':'post not exists'}, status=status.HTTP_400_BAD_REQUEST)
    
class PostViewLikesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id is None:
            return Response({'error':'no post id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_object = get_object_or_404(Post, id=post_id)
        except Exception as e:
            return Response({'error':'post not exists'}, status=status.HTTP_400_BAD_REQUEST)
        likes = post_object.like_set.filter(is_like=True)
        num_likes = likes.count()
        return Response({'num_likes': num_likes}, status=status.HTTP_200_OK)
        return redirect(request.META.get('HTTP_REFERER'))
    

class PostCreateCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        comment_on_post = request.POST.get('comment', None)
        if post_id is None or comment_on_post is None:
            return Response({'error':'no post id or comment missing'}, status=status.HTTP_400_BAD_REQUEST)
        Comment.objects.create(user=request.user, post_id=post_id , text=comment_on_post)
        return Response({'msg':comment_on_post}, status=status.HTTP_201_CREATED)


class HomeNewsFeedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.filter(is_active=True).exclude(user=user)
        serializer = NewFeedsPostSerializer(post, context={'request': request}, many=True )
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostEditCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id', None)
        if comment_id is None: #or comment_on_post is None:
            return Response({'error':'no post id missing'}, status=status.HTTP_400_BAD_REQUEST)
        comment_obj = get_object_or_404(Comment, user=request.user, pk=comment_id)
        serializer = CommentUpdateSerializer(instance=comment_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No comment exists'},status=status.HTTP_400_BAD_REQUEST)
    



class PostDeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id', None)
        if comment_id is None:
            return Response({'error':'no post id or comment missing'}, status=status.HTTP_400_BAD_REQUEST)
        comment_obj = get_object_or_404(Comment, user=request.user, pk=comment_id)
        serializer = CommentUpdateSerializer(instance=comment_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No comment exists'},status=status.HTTP_400_BAD_REQUEST)
        
    

class PostCommentsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comment_set.filter(is_active=True)
        serializer = CommentsViewSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    

class SavePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id is None:
            return Response({'error':'Post id is missing'})
        try:
            save_post = get_object_or_404(SavedPost, user = request.user, post_id=post_id)
        except Exception as e:
            save_post = SavedPost.objects.create(user=request.user, post_id=post_id)
            serializer = SavedPostSerializer(save_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error':'Already saved the post!!'}, status=status.HTTP_302_FOUND)
    


class UnSavePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def patch(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id is None:
            return Response({'error':'Post id is missing'})
        save_post = get_object_or_404(SavedPost, user = request.user, post_id=post_id)
        serializer = SavedPostSerializer(instance=save_post,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
class ViewSavePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        save_post = SavedPost.objects.filter(user=request.user, is_save=True)
        serializer = SavedPostSerializer(save_post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class GoogleLoginCallbackView(APIView):
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        self.permission_classes = [IsAuthenticated]
        login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        refresh = RefreshToken.for_user(user)
        # response = redirect("http://localhost:3000/newfeeds?access_token={}&refresh_token={}".format(str(refresh.access_token),str(refresh)))
        response = redirect("https://mutahharinstacloneservice-dot-cloud-work-314310.ew.r.appspot.com/newfeeds?access_token={}&refresh_token={}".format(str(refresh.access_token),str(refresh)))
        # print(response)
        return response