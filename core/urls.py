from django.urls import path
from .views import (
    CreatePostView, UserPostsView, UpdatePostView, UserDeletePostsView, 
    FollowDoneView, UnfollowDoneView,
    PostLikeView, PostUnLikeView, PostViewLikesView,
    PostCreateCommentView, PostEditCommentView, PostCommentsView, 
    SavePostView, UnSavePostView, ViewSavePostView, HomeNewsFeedView, GoogleLoginCallbackView
    )
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('follow/done/', view = FollowDoneView.as_view(), name='follow_view'),
    path('unfollow/done/', view = UnfollowDoneView.as_view(), name='unfollow_view'),
    path('create_post/', view = CreatePostView.as_view(), name = 'create_post'),
    path('posts/', view = UserPostsView.as_view(), name = 'view_posts'),
    path('update_post/<uuid:pk>/', view = UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<uuid:pk>/', view = UserDeletePostsView.as_view(), name='update_post'),
    path('like/<uuid:post_id>/', view = PostLikeView.as_view(), name='post_like_view'),
    path('unlike/<uuid:post_id>/', view = PostUnLikeView.as_view(), name='post_unlike_view'),
    path('view_likes/<uuid:post_id>/', view = PostViewLikesView.as_view(), name='view_likes_view'),
    path('comment/<uuid:post_id>/', view = PostCreateCommentView.as_view(), name='comment_on_post_view'),
    path('view_comment/<uuid:post_id>/', view = PostCommentsView.as_view(), name='view_comment_on_post_view'),
    path('edit_comment/<uuid:comment_id>/', view = PostEditCommentView.as_view(), name='edit_comment_on_post_view'),
    path('delete_comment/<uuid:comment_id>/', view = PostCommentsView.as_view(), name='view_comment_on_post_view'),
    path('save_post/<uuid:post_id>/', view = SavePostView.as_view(), name='save_post_view'),
    path('unsave_post/<uuid:post_id>/', view = UnSavePostView.as_view(), name='unsave_post_view'),
    path('view_save_post/', view = ViewSavePostView.as_view(), name='view_save_post_view'),
    path('newsfeed/', view = HomeNewsFeedView.as_view(), name='newsfeed_view'),
    path('generate_token/', view = GoogleLoginCallbackView.as_view(), name='jwt_generation_view'),
    
] 