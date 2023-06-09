from django.db import models
from django.contrib.auth import get_user_model
import uuid
from crum import get_current_user
from django.contrib.auth.models import User
# from storages.backends.gcloud import GoogleCloudStorage
from django.core.files.storage import default_storage
User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    picture = models.ImageField(upload_to='users_pictures', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, editable=False, related_name='posts')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return str(self.user)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is None:
            user = User.objects.first()
        self.user = user    
        super(Post, self).save(*args,**kwargs)

    @property
    def likes_count(self):
        return self.like_set.filter(post__is_active=True).count()
    
    @property
    def comments_count(self):
        return self.comment_set.filter(post__is_active=True).count()


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_set', editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.text)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is None:
            user = User.objects.first()
        self.user = user    
        super(Comment, self).save(*args,**kwargs)



class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_like = models.BooleanField(default=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_set', editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self) -> str:
        return str(self.is_like)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = User.objects.first()
        self.user = user    
        super(Like, self).save(*args,**kwargs)
        

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE)
    # is_follow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self) -> str:
        return f"{self.user} --> {self.followed}"
    
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is None:
            user = User.objects.first()
        self.user = user    
        super(Follow, self).save(*args,**kwargs)
        

class SavedPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    is_save = models.BooleanField(default=True)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.pk)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is None:
            user = User.objects.first()
        self.user = user    
        super(SavedPost, self).save(*args, **kwargs)