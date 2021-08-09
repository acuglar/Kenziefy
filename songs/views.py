from django.http import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from songs.models import Artist, Song
from songs.serializers import SampleSerializer, ArtistSerializer, SongSerializer, ArtistSongsSerializer
import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        serializer = SampleSerializer(data=request.data)
        serializer.is_valid() 
        serializer.data  

        return Response({"message": "This is a POST method"})


class ParamView(APIView):
    def get(self, request, name):
        return Response({"get method message": f"Hello {name}"})
        
    def post(self, request, name):
        return Response({"post method message": f"Hello {name}"})


class KenziefyArtistView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        # <QuerySet [<Artist: Dio>, <Artist: Black Sabbath>, <Artist: Pink Floyd>]> 

        # artist = artists[0].__dict__
        # {'_state': <django.db.models.base.ModelState object at 0x7fb5b6be6640>, 'id': 1, 'name': 'Dio'}
        # return Response(artist)
        # Object of type ModelState is not JSON serializable

        # ipdb.set_trace()
        
        # artist.pop('_state')

        # remoção teria que ser feito um a um => serializer
        # serializer retorna um padrão para a chamada na view

        serialized = ArtistSerializer(artists, many=True)
        # sem attrib many: AttributeError
        # artists é um QuerySet: list => many=True
        # ipdb.set_trace()

        return Response(serialized.data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        # data indica não tratar-se de objeto

        if not serializer.is_valid():
            # caso campo faltante: "this field is required"
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # ipdb.set_trace()
        # ipdb> request.data
        # {'name': 'Teste38', 'formed_in': 2006, 'status': 'Active', 'outro': 'pudim'}
        # ipdb> serializer.data
        # {'name': 'Teste38', 'formed_in': 2006, 'status': 'Active'}
        # ipdb> serializer.validated_data
        # OrderedDict([('name', 'Teste38'), ('formed_in', 2006), ('status', 'Active')])
        artist = Artist.objects.get_or_create(**serializer.validated_data)[0]
        
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

class KenziefySongView(APIView):
    def get(self, request):
        songs = Song.objects.all()

        serialized = SongSerializer(songs, many=True)

        return Response(serialized.data) 
    
    def post(self, request):
        serializer = ArtistSongsSerializer(data=request.data)
        # data indica não tratar-se de objeto

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        artist = Artist.objects.get_or_create(**serializer.validated_data)[0]
        
        serializer = ArtistSongsSerializer(artist)
        ipdb.set_trace()
        return Response(serializer.data)

        # SEMPRE validated_data quando criação 
        # data apenas para retorno