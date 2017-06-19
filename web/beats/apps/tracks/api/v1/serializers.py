""" Serializers for Tracks APIs """

from rest_framework import serializers

from ...models import Genre, Track, FileUpload


class GenreSerializer(serializers.ModelSerializer):
    """ Serializer for Model Genre """

    class Meta:
        """ Meta Genre Serializer """
        model = Genre
        fields = ('id', 'name')
        read_only = 'id'

class TrackSerializer(serializers.ModelSerializer):
    """ Serializer for generic Model Track data """

    class Meta:
        """ Meta Track Serializer """
        model = Track
        fields = ('id', 'title', 'genre', 'release_date', 'is_purchasable', 'purchase_price')


class TrackDetailSerializer(serializers.ModelSerializer):
    """ Serializer for detailed Model Track data """

    class Meta:
        """ Meta Track Detail Serializer """
        model = Track
        fields = (
            'id', 'title', 'genre', 'release_date', 'is_purchasable',
            'purchase_price', 'is_available_for_mix', 'is_active',
            'date_created', 'date_updated')


class FileUploadSerializer(serializers.ModelSerializer):
    """ Serializer for Model Track File """

    class Meta:
        """ Meta Track File Serializer """
        model = FileUpload
        fields = ('name', 'doc', 'size')
