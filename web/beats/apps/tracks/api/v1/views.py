""" API Views for Tracks app """
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from ...models import Track
#from beats.apps.tracks.models import Track
from .serializers import TrackSerializer, TrackDetailSerializer


class TrackListAPI(generics.ListAPIView):
    """ API endpoint for listing all tracks """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackDetailAPI(generics.RetrieveAPIView):
    """ API endpoint for GET on a single track """
    serializer_class = TrackDetailSerializer

    def get_object(self):
        return get_object_or_404(Track, pk=self.kwargs['pk'])

class TrackUploadAPI(APIView):
    """ API endpoint for POST to upload a file """
    def post(self, request, format=None):
        # TODO: handle file upload to media dir
        return Response(status=status.HTTP_200_OK)

