# from django.test import TestCase

# # Create your tests here.
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import AccessToken
# from .models import Post, Comment
# from .serializer import CommentsViewSerializer

# class PostCommentsViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.post = Post.objects.create(user=self.user, title='Test Post', body='Test body')
#         self.comment1 = Comment.objects.create(post=self.post, user=self.user, text='Test comment 1')
#         self.comment2 = Comment.objects.create(post=self.post, user=self.user, text='Test comment 2')
#         self.url = reverse('post-comments', kwargs={'post_id': self.post.id})
#         self.access_token = str(AccessToken.for_user(self.user))

#     def test_get_comments(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = CommentsViewSerializer([self.comment1, self.comment2], many=True, context={'request': response.wsgi_request}).data
#         self.assertEqual(response.data, expected_data)

#     def test_get_comments_unauthenticated(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
