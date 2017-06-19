""" Unit Tests for Tracks API """
import json

from django.core.urlresolvers import reverse
from rest_framework.test import APIClient, APITestCase

from beats.apps.tracks.models import FileUpload


class TracksListTestCase(APITestCase):
    """ Test Listing Tracks from Beatport API """

    def setUp(self):
        """ Set Up """
        self.client = APIClient()

    def test_get_track_list(self):
        """ Test API for track list, returns only basic info (name) """
        url = reverse('api:tracks:track-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertGreater(len(data), 0)
        get_key = data[0].get('name', None)
        self.assertIsNotNone(get_key)
        self.assertRaises(KeyError, lambda: data[0]['sku'])
        self.assertRaises(KeyError, lambda: data[0]['purchasable'])


class TracksDetailTestCase(APITestCase):
    """ Test Track API by specific PK, returns detailed info """

    def setUp(self):
        self.client = APIClient()

    def test_track_by_nonexistent_pk(self):
        """ Track not found should return 404 """
        nonexistent_pk = 0
        url = reverse('api:tracks:track-detail', kwargs={'pk': nonexistent_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), [])

    def test_track_by_existing_pk(self):
        """ Track found should return 200 with details """
        existing_pk = 8650404
        url = reverse('api:tracks:track-detail', kwargs={'pk': existing_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['purchasable'], True)
        self.assertEqual(response.data['type'], 'track')
        self.assertEqual(response.data['sku'], 'track-8650404')


class FileUploadTestCase(APITestCase):
    """ Upload File to Media dir """

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        file_query = FileUpload.objects.all()
        for file_obj in file_query:
            if file_obj:
                file_obj.doc.delete()

    def test_put_invalid_data(self):
        """ Test FileUpload with bad input """
        url = reverse('api:tracks:track-upload')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FileUpload.objects.all().count(), 0)

    def test_put_valid_data(self):
        """ Test FileUpload with correct input """
        url = reverse('api:tracks:track-upload')
        with open('./fixtures/hello.txt', 'rb+') as docfile:
            response = self.client.put(
                url, data={'doc': docfile, 'name': 'hello3.txt'},
                format='multipart')
        self.assertEqual(response.status_code, 202)

        # Check file saved to db
        self.assertEqual(FileUpload.objects.all().count(), 1)
        file_obj = FileUpload.objects.first()
        self.assertEqual(file_obj.name, 'hello.txt')
        self.assertEqual(file_obj.size, 29)
