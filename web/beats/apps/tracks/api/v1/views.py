""" API Views for Tracks app """
import json

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
import requests
from requests_oauthlib import OAuth1

from beats.settings.env import (
    OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
)

from ...models import Track, FileUpload
from ...forms import FileUploadForm 
from .serializers import (
    TrackSerializer, TrackDetailSerializer, FileUploadSerializer
)

class TrackListAPI(APIView):
    """ API endpoint for listing all tracks """
    auth = OAuth1(
        OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    tracks_url = 'https://oauth-api.beatport.com/catalog/3/tracks'
    def get(self, request, *args, **kwargs):
        bp_response = requests.get(self.tracks_url, auth=self.auth)
        full_results = bp_response.json()['results']
        filtered_data = []
        for track in full_results:
            filtered_data.append({'name': track['name']})
        return Response(json.dumps(filtered_data), status=bp_response.status_code)

class TrackDetailAPI(generics.RetrieveAPIView):
    """ API endpoint for GET on a single track """
    auth = OAuth1(
        OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    tracks_url = 'https://oauth-api.beatport.com/catalog/3/tracks?id='
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        bp_response = requests.get(self.tracks_url + pk, auth=self.auth)
        if len(bp_response.json()['results']) != 1:
            return Response(bp_response.json()['results'], status=status.HTTP_404_NOT_FOUND)
        return Response(bp_response.json()['results'][0], status=bp_response.status_code)


class TrackUploadAPI(APIView):
    """ API endpoint for PUT to upload a file """
    serializer_class = FileUploadSerializer

    def put(self, request, *args, **kwargs):
        """ PUT as idimpotent operation, replace file if one exists """
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.FILES['doc'].name
            try:
                instance = FileUpload.objects.get(name=name)
                instance.doc.delete(save=False) # remove old file, but don't save yet
                instance.doc = request.FILES['doc']
                instance.size = request.FILES['doc'].size
                instance.save()
            except FileUpload.DoesNotExist:
                instance = FileUpload.objects.create(name=name, doc=request.FILES['doc'], size=request.FILES['doc'].size)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
