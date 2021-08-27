# Kenziefy 002_models_and_relations_

## criando model
1. ao criar uma model, necessário fazer as migrations
```sh
./manage.py makemigrations  # No changes detect
```
2. antes, declarar o app em settings.INSTALLED_APPS
```sh
./manage.py showmigrations  
./manage.py makemigrations  # verificando alterações em models e criando um script para posteriormente update no db
./manage.py migrate  # aplicando alterações
./manage.py showmigrations

# arquivo db.sqlite3 criado. Verificar com postgresql
```

## shell 

```py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
```

```py
./manage.py shell
from songs.models 

In [1]: from songs.models import Song

In [2]: s1 = Song.objects.create(title="Fear Of The Dark", artist="Iron Maiden")  # criando song s1 em db

In [3]: s2 = Song.objects.create(title="Stairway To Heaven", artist="Led Zeppelin")

In [4]: s1
Out[4]: <Song: Song object (1)>  # número refere-se ao id

# para visual, necessário criar na model um método de representação __str__
# entrando no shell novamente:

In [1]: from songs.models import Song

In [2]: s1
NameError: name 's2' is not defined

In [3]: s3 = Song.objects.create(title="Pynk Floid", artist="Wish You In Here")

In [5]: s3
Out[5]: <Song: Pynk Floid - Wish You In Here>

# s1, s2, s3 criados em db

# OUTRA FORMA
In [6]: Song(title="Last Kiss", artist="Pearl Jam")
Out[6]: <Song: Last Kiss - Pearl Jam>
# apenas invoke

In [7]: s4 = Song(title="Last Kiss", artist="Pearl Jam")
# instanciando

In [9]: s4.save()
# salvando em db
# ESSA FORMA É MAIS PERFORMATICA PORQUE ACESSA DB APENAS EM .save()

# como até então não há constraint definida, instâncias podem ser repetidas
# Para contornar isso get_or_create():

In [10]: s5 = Song.objects.get_or_create(title="Last Kiss", artist="Pearl Jam")
# se houver registro, retorna o objeto; se 

In [11]: s5
Out[11]: (<Song: Last Kiss - Pearl Jam>, False)  # False -> já existe no db

In [12]: s6 = Song.objects.get_or_create(title="Come as You Are", artist="Nirvana")

In [13]: s6
Out[13]: (<Song: Come as You Are - Nirvana>, True)  # True -> criando no db

In [14]: s6 = Song.objects.get_or_create(title="In Bloom", artist="Nirvana")


```
A criação de um artista pode ser repetida, no entanto isso implica consequências. e.g.: erro de digitação ->  \<Song: In Bloom - Nirvana>, \<Song: In Bloom - Mirvana> 

### Relacionamento artist 1:N song:
```py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

# $ ./manage.py makemigrations
# $ ./manage.py migrate
# django.db.utils.IntegrityError: The row in table 'songs_song' with primary key '1' has an invalid foreign key: songs_song.artist_id contains a value 'Iron Maiden' that does not have a corresponding value in songs_artist.id.

# recurso grosseiro: deletar db.sqlite3 e passar migrate novamente



```

```py
In [1]: from songs.models import Song, Artist

In [2]: a1 = Artist.objects.create(name="Guns N\' Roses")

In [3]: s1 = Song.objects.create(title="Welcome To The Jungle")
IntegrityError: NOT NULL constraint failed: songs_song.artist_id
# instância de artista precisa ser passada

In [3]: s1 = Song.objects.create(title="Welcome To The Jungle", artist=a1)

In [4]: s1
Out[4]: <Song: Welcome To The Jungle>

In [5]: s1.artist
Out[5]: <Artist: Guns N\' Roses>

# Por padrão campos relacionados são não nulos (null=False). 
# comportamentos distintos necessitam ser especificados

# class Artist(models.Model):
#     name = models.CharField(max_length=255, null=True, blank=True)
# blank -> permitir campo vazio quando instanciândo e forms

# Acessando lado inverso da relação:
In [8]: a1.song_set
Out[8]: <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager at 0x7f2815f21190>

In [9]: a1.song_set.all()
Out[9]: <QuerySet [<Song: Welcome To The Jungle>]>

# POR PADRÃO `_set`
# para mudar definir o parâmetro related_name (songs.model.Song)

# alterações em models -> makemigrations, migrate
# sair do shell e entrar novamente

In [8]: a1 = Artist.objects.get(name="Guns N' Roses")

In [9]: a1.songs.all()
Out[9]: <QuerySet [<Song: Welcome To The Jungle>]>
```

### relacionamento artist 1:1 bio

```py
In [1]: from songs.models import Artist, Biography

In [3]: artist = Artist.objects.get(name="Guns N\' Roses")
# get -> já existe "Guns N\' Roses"
# DEFAULT relacionamentos null=False => artist must exists to biography

# o relacionamento é bilateral, no entanto, convém racionalizar a lógica da orientação
# e.g. se biography em Artist, não poderia criar artist sem criar bio. 
# Não faz sentido existir bio antes de artist  

In [4]: bio = Biography.objects.create(description="bio Guns", artist=artist)

In [5]: bio
Out[5]: <Biography: Biography object (1)>

In [6]: bio.artist
Out[6]: <Artist: Guns N' Roses>

In [7]: artist.biography
Out[7]: <Biography: Biography object (1)>
```

### relacionamento song N:N playlist

```py
In [1]: from songs.models import Song, Playlist

In [2]: songs = Song.objects.all()

In [3]: songs
Out[3]: <QuerySet [<Song: Welcome To The Jungle>]>

In [4]: songs = Song.objects.count()

In [5]: songs
Out[5]: 1

In [6]: playlist = Playlist.objects.create(title="first playlist")
# null=True, não necessário especificação

In [7]: song = Song.objects.first()

In [8]: song
Out[8]: <Song: Welcome To The Jungle>

In [9]: playlist.songs.add(song)
# relacionando song to playlist

In [10]: playlist.songs.all()
Out[10]: <QuerySet [<Song: Welcome To The Jungle>]>

In [11]: playlist.songs.remove(song)
# removendo objeto especificado

In [11]: playlist.songs.clear()
# removendo todos songs de playlist

In [12]: playlist.songs.all()
Out[12]: <QuerySet []>

In [13]: playlist.songs.add(song)

In [14]: playlist.songs.add(song)

In [15]: playlist.songs.all()
Out[15]: <QuerySet [<Song: Welcome To The Jungle>]>
# repetição não aceita 

# tabela pivo para ManyToMany é criado no padrão app_tabela (songs_playlist_songs)

In [16]: song.playlist
AttributeError: 'Song' object has no attribute 'playlist'
# related_name não declarado

In [17]: song.playlist_set
Out[17]: <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x7fa3c32dd6a0>

# Playlist.songs(related_name="playlists")
In [18]: song.playlists
Out[18]: <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x7fb2728a4ac0>
```

### instânciando muitas de uma vez
```py
In [2]: from songs.models import Artist, Song, Playlist

In [3]: artists = Artist.objects.all()

In [4]: artists
Out[4]: <QuerySet [<Artist: Guns N' Roses>, <Artist: RHCP>]>

In [26]: artist = Artist.objects.first()

In [27]: song1
Out[27]: <Song: Welcome To The Jungle>

In [28]: song2 = Song.objects.create(title="November Rain", artist=artist)

In [29]: song2
Out[29]: <Song: November Rain>

In [33]: playlist.songs.clear()

In [34]: playlist.songs.add(song1, song2)
```
