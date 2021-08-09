from django.urls import path
from .views import SampleView, ParamView, KenziefyArtistView, KenziefySongView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<str:name>/', ParamView.as_view()),
    path('kenziefy/', KenziefyArtistView.as_view()),
    path('kenziefy/songs/', KenziefySongView.as_view()),
]
