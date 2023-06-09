from rest_framework import serializers
from .models import Post, Follow, Comment, SavedPost
from user.models import User

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    user_profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = Post  
        fields = ('id', 'description', 'picture', 'video', 'is_active', 'location', 'created_at', 'updated_at', 'user', 'username', 'user_profile_picture', 'likes_count', 'comments_count')
        read_only_fields = ('created_at', 'updated_at', 'user')
        extra_kwargs = {'is_active': {'default': True}}
        
    def validate(self, data):
        if data.get('picture') and data.get('video'):
            raise serializers.ValidationError("Please upload either a picture or a video, but not both.")
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return super().update(instance, validated_data)
    
    def get_likes_count(self, obj):
        return obj.like_set.filter(is_like=True).count()
    
    def get_comments_count(self, obj):
        return obj.comment_set.filter(is_active=True).count()
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_user_profile_picture(self, obj):
        if obj.user.profile_picture:
            return self.context['request'].build_absolute_uri(obj.user.profile_picture.url)
        return None

class NewFeedsPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_profile_picture = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'description', 'picture', 'video', 'is_active', 'location', 'created_at', 'updated_at', 'user', 'username','user_profile_picture', 'likes_count', 'comments_count')
        read_only_fields = ('created_at', 'updated_at', 'user')
        extra_kwargs = {'is_active': {'default': True}}

    def get_username(self, obj):
        return obj.user.username
    
    def get_user_profile_picture(self, obj):
        if obj.user.profile_picture:
            return self.context['request'].build_absolute_uri(obj.user.profile_picture.url)
        return None
    
    def get_likes_count(self, obj):
        return obj.like_set.filter(is_like=True).count()
    
    def get_comments_count(self, obj):
        return obj.comment_set.filter(is_active=True).count()
    

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'


class CommentsViewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    username = serializers.ReadOnlyField(source='user.username')
    user_profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = Comment
        fields='__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    
    
class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_save = validated_data.get('is_save', instance.is_save)
        instance.save()
        return instance
