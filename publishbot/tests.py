import pdb
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

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

        self.publication1 = Publication.objects.create(text='Test publication 1', image='image.jpg', video='',
                                                       url='http://example.com', priority=1, canceled=False,
                                                       publication_type='text', score=10)
        self.publication2 = Publication.objects.create(text='Test publication 2', image='', video='',
                                                       url='http://example.com', priority=2, canceled=False,
                                                       publication_type='text', score=20)

    def tearDown(self):
        for publication in Publication.objects.all():
            # delete the image file
            try:
                publication.image.delete()
            except ValueError:
                pass

    def test_get_all_publications(self):
        url = reverse('publication-list')
        response = self.client.get(url)
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test  get single publication with id
    def test_get_single_publication(self):
        # reverse() will generate the URL for us
        url = reverse('publication-detail', args=[self.publication1.id])
        response = self.client.get(url)
        publication = Publication.objects.get(id=self.publication1.id)
        serializer = PublicationSerializer(publication)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_publication(self):
        url = reverse('publication-list')
        # create a test image file
        image = SimpleUploadedFile(name='test_image.jpg', content=open('media/test_image.jpg', 'rb').read(),
                                   content_type='image/jpeg')
        data = {'text': 'New publication', 'image': image, 'video': '', 'url': 'http://example.com',
                'priority': 1, 'canceled': False, 'publication_type': 'image', 'score': 10}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test if the publication is created
        self.assertEqual(Publication.objects.count(), 3)  # 2 publications created in setUp()
        # test if the publication is created with all the correct data
        publication = Publication.objects.get(id=3)
        self.assertEqual(publication.url, 'http://example.com')
        self.assertEqual(publication.priority, 1)
        self.assertEqual(publication.canceled, False)
        self.assertEqual(publication.publication_type, 'image')
        self.assertEqual(publication.score, 10)
        self.assertEqual(publication.text, 'New publication')
        # test if the image file is created
        self.assertIsNotNone(publication.image)
        # delete the image file
        publication.image.delete()

    def test_update_publication(self):
        url = reverse('publication-detail', args=[self.publication1.id])
        data = {'text': 'Updated publication', 'image': '', 'video': '', 'url': '',
                'priority': 3, 'canceled': False, 'publication_type': 'image', 'score': 10}
        response = self.client.put(url, data)
        # test the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test if the publication is updated
        publication = Publication.objects.get(id=self.publication1.id)
        self.assertEqual(publication.text, 'Updated publication')
        self.assertEqual(publication.priority, 3)


