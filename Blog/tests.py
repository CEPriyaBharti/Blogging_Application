from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment, Like

class PostViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New post', 'content': 'This is a new post'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        url = reverse('post-detail', kwargs={'pk': post.pk})
        data = {'title': 'Updated post', 'content': 'Updated content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CommentViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)

    def test_create_comment(self):
        url = reverse('comment-list', kwargs={'post_id': self.post.pk})
        data = {'text': 'This is a test comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comments(self):
        Comment.objects.create(post=self.post, author=self.user, text='This is a test comment')
        url = reverse('comment-list', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class LikeViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.post = Post.objects.create(title='Post 1', content='Content 1', author=self.user)

    def test_create_like(self):
        url = reverse('like-list', kwargs={'post_id': self.post.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_likes(self):
        Like.objects.create(post=self.post, author=self.user)
        url = reverse('like-list', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
