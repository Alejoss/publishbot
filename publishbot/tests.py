import pdb
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User

from publishbot.models import Publication
from publishbot.serializers import PublicationSerializer


class TestClientWithToken(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class PublicationAPIViewTestCase(TestClientWithToken):
    def setUp(self):
        super().setUp()

        self.publication1 = Publication.objects.create(text='Test publication 1', image='image.jpg', video='video.mp4',
                                                       url='http://example.com', priority=1, canceled=False,
                                                       publication_type='type1', score=10)
        self.publication2 = Publication.objects.create(text='Test publication 2', image='image.jpg', video='video.mp4',
                                                       url='http://example.com', priority=2, canceled=False,
                                                       publication_type='type2', score=20)

    def test_get_all_publications(self):
        url = reverse('publication-list')
        response = self.client.get(url)
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_publication(self):
        url = reverse('publication-detail', args=[self.publication1.id])
        response = self.client.get(url)
        publication = Publication.objects.get(id=self.publication1.id)
        serializer = PublicationSerializer(publication)
        pdb.set_trace()
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_publication(self):
    #     url = reverse('publication-list')
    #     data = {'text': 'New publication', 'image': 'image.jpg', 'video': 'video.mp4', 'url': 'http://example.com',
    #             'priority': 1, 'canceled': False, 'publication_type': 'type1', 'score': 10}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_update_publication(self):
    #     url = reverse('publication-detail', args=[self.publication1.id])
    #     data = {'text': 'Updated publication', 'image': 'image.jpg', 'video': 'video.mp4', 'url': 'http://example.com',
    #             'priority': 1, 'canceled': False, 'publication_type': 'type1', 'score': 10}
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_delete_publication(self):
    #     url = reverse('publication-detail', args=[self.publication1.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
