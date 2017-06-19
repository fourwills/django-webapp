""" API Views for Tracks app """
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.conf import settings


from ...models import Track, FileUpload
from ...forms import FileUploadForm 
from .serializers import (
    TrackSerializer, TrackDetailSerializer, FileUploadSerializer
)

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
