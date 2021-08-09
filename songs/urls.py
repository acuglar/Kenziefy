from django.urls import path
from .views import SampleView, ParamView, ArtistView, ArtistDetailView, PlaylistView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<str:name>/', ParamView.as_view()),
    path('artists/', ArtistView.as_view()),
    path('artists/<int:artist_id>', ArtistDetailView.as_view()),
    path('playlists/', PlaylistView.as_view())
]

