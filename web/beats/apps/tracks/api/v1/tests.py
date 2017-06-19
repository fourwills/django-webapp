from datetime import datetime

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from beats.apps.tracks.models import Genre, Track, FileUpload


class TracksListTestCase(APITestCase):

    def setUp(self):
        """ Set Up """
        self.client = APIClient()

    def tearDown(self):
        """ Clean up """
        Genre.objects.all().delete()
        Track.objects.all().delete()

    def test_get_track_list_empty_items(self):
        """ Test API for blank track list """
        url = reverse('api:tracks:track-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_track_list_with_items(self):
        """ Test API for blank track list """

        # Test one object appears in list
        genre_obj = Genre.objects.create(name='house')
        Track.objects.create(
            release_date=datetime.now(),
            purchase_price=10.75,
            genre=genre_obj,
            title="First Here"
        )
        url = reverse('api:tracks:track-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "First Here")
        self.assertEqual(response.data[0]['purchase_price'], '10.75')

        # Test a second object appears in list
        Track.objects.create(
            release_date=datetime.now(),
            purchase_price=11,
            genre=genre_obj,
            title="Second Here"
        )
        url = reverse('api:tracks:track-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['title'], "Second Here")
        self.assertEqual(response.data[1]['purchase_price'], '11.00')


class TracksDetailTestCase(APITestCase):
    """ Test Track API by specific PK, returns detailed info """

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Genre.objects.all().delete()
        Track.objects.all().delete()

    def test_get_track_by_nonexistent_pk(self):
        """ Track not found should return 404 """
        nonexistent_pk = 999  # Should have been cleaned up from test tearDown()
        url = reverse('api:tracks:track-detail', kwargs={'pk': nonexistent_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_get_track_by_existing_pk(self):
        """ Track found should return 200 with details """
        genre_obj = Genre.objects.create(name='house')
        Track.objects.create(
            release_date=datetime.now(),
            purchase_price=10.75,
            genre=genre_obj,
            title="I am here!"
        )
        track_obj = Track.objects.first()
        existing_pk = track_obj.pk
        url = reverse('api:tracks:track-detail', kwargs={'pk': existing_pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'I am here!')
        self.assertEqual(response.data['is_available_for_mix'], False)
        self.assertEqual(response.data['is_purchasable'], False)

class FileUploadTestCase(APITestCase):
    """ Upload File to Media dir """

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        FileUpload.objects.all().delete() 

    def test_put_invalid_data(self):
        url = reverse('api:tracks:track-upload')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
    
    def test_put_valid_data(self):
        url = reverse('api:tracks:track-upload')
        with open('./fixtures/hello.txt', 'rb+') as docfile:
            response = self.client.put(
                url, data={'doc': docfile, 'name':'hello3.txt'}, format='multipart')
        self.assertEqual(response.status_code, 202)
        