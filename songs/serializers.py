from rest_framework import serializers
from collections import OrderedDict

class SampleSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField(required=True)

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # wo read_only -> request: "this field is required"
    name = serializers.CharField()
    formed_in = serializers.IntegerField()  # input default 2021 foi colocado manualmente em migrate 
    status = serializers.CharField()  # input default 'Active' foi colocado manualmente em migrate

class SongSerializer(serializers.Serializer):
    title = serializers.CharField()
    # artist_id = serializers.IntegerField()
    # artist = serializers.CharField() 
    """
    [
        {
            "title": "Holy Diver",
            "artist_id": 1,
            "artist": "Artist object (1)" # __str__ => "artist": "Dio"
        },
        ...
    ]
    """
    # Essa não é a melhor forma de trabalhar view de relacionamentos.
    # Usar os metódos de serializers para relacionamento na ref artist
    # artist = serializers.PrimaryKeyRelatedField(read_only=True)  # id. artist_id
    # artist = serializers.StringRelatedField(read_only=True)  # invoca __str__
    artist = ArtistSerializer() 

class SongSimpleSerializer(serializers.Serializer):    
    title = serializers.CharField()
    
    
class ArtistSongsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    formed_in = serializers.IntegerField(write_only=True)
    status = serializers.CharField()
    musics = SongSerializer(many=True, read_only=True, source='songs')
    # source indica qual atributo sera buscado o valor, neste caso songs por musics
    
    total_songs = serializers.SerializerMethodField()
    #  SerializerMethodField indica via método 
    
    def get_total_songs(self, obj):
        if (isinstance(obj, OrderedDict)):
            return 0
        return { 'count': obj.songs.count()}
