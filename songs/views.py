from django.http import response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from songs.models import Artist, Song, Playlist
from songs.serializers import SampleSerializer, ArtistSerializer, SongSerializer, ArtistSongsSerializer, PlaylistSerializer
import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        serializer = SampleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer.data
        # ipdb.set_trace()
  
        # return Response({"message": "This is a POST method"})
        return Response(serializer.data)


class ParamView(APIView):
    def get(self, request, name):
        return Response({"get method message": f"Hello {name}"})
        
    def post(self, request, name):
        return Response({"post method message": f"Hello {name}"})


class ArtistView(APIView):
    """ se query_params, retorna objeto else retorna todos """
    def get(self, request):
    
        """ primeiro modo """
    # def get(self, request, artist_id=''):
    #     if artist_id:
    #         artist = Artist.objects.get(id=artist_id)
    #         serializer = ArtistSongsSerializer(artist)
    #         return Response(serializer.data)

    #     artist = Artist.objects.all()
    #     serializer = ArtistSongsSerializer(artist)
    #     return Response(serializer.data)

        """ django.shortcuts (tratamento de exceção 404) """
    # def get(self, request, artist_id=''):
    #     if artist_id:
    #         artist = get_object_or_404(Artist, id=artist_id)
    #         serializer = ArtistSongsSerializer(artist)
    #         return Response(serializer.data)

    #     artist = Artist.objects.all()
    #     serializer = ArtistSongsSerializer(artist)
    #     return Response(serializer.data)

    # Preferível dividir as tarefas em rotas sem (ArtistView) e com query_params (ArtistDetailView)  

        if request.query_params:
            artist = Artist.objects.filter(name__icontains=request.query_params.get('name', ''))
        else:
            artist = Artist.objects.all()
        
        serialized = ArtistSongsSerializer(artist, many=True)
        return Response(serialized.data)
    
    def post(self, request):
        serializer = ArtistSongsSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        songs = validated_data.pop('songs')
        
        artist = Artist.objects.get_or_create(**serializer.validated_data)[0]
        
        song_list = []
        for song in songs:
            # Song.objects.get_or_create(**song, artist=artist)
            song = Song(**song, artist=artist)
            song_list.append(song)
            
        Song.objects.bulk_create(song_list)    
        # bulk_create é mais performático que get_or_create no for porque faz um único acesso ao banco
            
        serializer = ArtistSongsSerializer(artist)
        return Response(serializer.data)
    
class ArtistDetailView(APIView):
    def get(self, request, artist_id=''):
        artist = get_object_or_404(Artist, id=artist_id)
        serializer = ArtistSongsSerializer(artist)
        return Response(serializer.data)
        
    def put(self, request, artist_id=''):
        serializer = ArtistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        artist = get_object_or_404(Artist, id=artist_id)
        artist.name = serializer.validated_data['name']
        artist.formed_in = serializer.validated_data['formed_in']
        artist.status = serializer.validated_data['status']

        artist.save()
        
        serializer = ArtistSongsSerializer(artist, many=True)
        
        return Response(serializer.data)
    
    def patch(self, request, artist_id=''): 
        serializer = ArtistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
        artist = Artist.objects.filter(id=artist_id)

        if not artist.exists():
            return Response({ 'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        artist.update(**serializer.validated_data)
        
        serializer = ArtistSongsSerializer(artist, many=True)
        
        return Response(serializer.data)
    
    def delete(self, request, artist_id):
        artist = get_object_or_404(Artist, id=artist_id)
        
        artist.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PlaylistView(APIView):
    def get(self, request):
        playlists = Playlist.objects.all()
        
        serializer = PlaylistSerializer(playlists, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        # especificação data indica que trata-se de dict, não uma instância
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        
        songs = validated_data.pop('songs')

        song_list = []
        
        for song in songs:
            artist = song.pop('artist')
            
            artist = Artist.objects.get_or_create(**artist)[0]
            # retorna tupla
            
            song = Song.objects.get_or_create(title=song['title'], artist=artist)[0]
            
            song_list.append(song)
            
        
        playlist = Playlist.objects.get_or_create(**validated_data)[0]
        playlist.songs.set(song_list)
        # set substitui
            
        serializer = PlaylistSerializer(playlist)
        
        return Response(serializer.data)
