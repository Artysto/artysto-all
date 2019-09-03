from django.urls import path
from . import views


app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('artists', views.artists, name='all_artists'),
    path('<int:ids>', views.album_id, name='album_id'),
    path('<int:ids>/favourite', views.favourite, name='favourite'),
    path('albums', views.albums, name='all_album'),
    path('songs', views.songs, name='all_songs'),
    path('<int:pk>/add-songs', views.SongCreate.as_view(), name='add-songs'),
    path('<int:album_id>/add-songs/<int:song_id>', views.delete_song, name='delete-songs'),
    path('base', views.base, name='base'),
    path('add-album', views.AlbumCreate.as_view(), name='add-album'),
    path('<int:pk>/delete', views.AlbumDelete.as_view(), name='delete-album'),
    path('<int:pk>/update-album', views.AlbumUpdate.as_view(), name='update-album'),
]

