from django.db import models


# CONVENTION: models são declaradas em singular 
class Song(models.Model):
    """ artist 1:N songs """
    title = models.CharField(max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="songs")     
    # primeito parametro model a ser relacionada
    # declaração Artist é válido desde que esteja a classe esteja abaixo da referência
    # declaração em string é capturada corretamente independentemente da ordem

    # segundo parâmetro política de deleção

    def __str__(self):
        return f'{self.title}'

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Biography(models.Model):
    """ artist 1:1 bio """
    description = models.TextField()
    # TextField não é restrito a 255 caracteres
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists")
    # on_delete não é requisito em ManyToMany   
    # ManyToMany DEFAULT -> null=True 

