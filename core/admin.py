from django.contrib import admin
from core.models import Like, Comment, Follow, Post, SavedPost

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'description', 'picture', 'location', 'user', 'created_at', 'updated_at', 'is_active')
    def get(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
class CommentModelAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('text', 'post', 'user', 'created_at', 'updated_at')

class LikeModelAdmin(admin.ModelAdmin):
    model = Like
    list_display = ('is_like', 'post', 'user', 'created_at', 'updated_at')

class FollowModelAdmin(admin.ModelAdmin):
    model = Follow
    list_display = ('user', 'followed', 'created_at', 'updated_at')

class SavedPostModelAdmin(admin.ModelAdmin):
    model = SavedPost
    list_display = ('post', 'user', 'saved_on')

admin.site.register(Like, LikeModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Follow, FollowModelAdmin)
admin.site.register(Post)
admin.site.register(SavedPost, SavedPostModelAdmin)
