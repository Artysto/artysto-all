from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.


def base(request):
    return render(request, 'music/base.html', context={})


def index(request):

    return render(request, 'music/index.html', context={'all_album': Album.objects.all()})


def artists(request):
    html = "<h1> This page is a listing of all artists that you can discover on this site<h1>"
    all_album = Album.objects.all()
    for album in all_album:
        html += "<li>" + album.artist + "</li>"

    return HttpResponse(html)


def albums(request):
    html = "<h1> This page is a listing of all albums that you can discover on this site<h1>"
    all_album = Album.objects.all()
    for album in all_album:
        html += "<li>" + "<a href ='/music/" + str(album.id) + "' >" + album.album_title + "</a>" + "</li>"

    return HttpResponse(html)


def album_id(request, ids):
    try:
        context = {'album': Album.objects.filter(id=ids)[0]}
        return render(request, 'music/album.html', context)
    except IndexError:
        raise Http404("What you are looking for doesn't even exist. How did you even get here? Don't drink and type")


def songs(request):
    all_albums = Album.objects.all()
    all_songs =[]
    for album in all_albums:
        all_songs += Song.objects.filter(album=album.id)
    return render(request, 'music/songs.html', context={'song_list': all_songs})


class SongCreate(CreateView):

    model = Song
    fields = [
        'song_title',
        'audio_file',
        'is_favorite',

    ]

    def form_valid(self, form):
        album = get_object_or_404(Album, pk=self.kwargs["pk"])
        form.instance.album = album
        return super().form_valid(form)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/album.html', {'album': album})


def favourite(request, ids):
    album = get_object_or_404(Album, id=ids)
    try:
        selected_song = album.song_set.get(id=request.POST['song'])
        selected_song.is_favourite = not selected_song.is_favourite
        selected_song.save()
        context = {'album': album}
        return render(request, 'music/album.html', context)
    except (IndexError, KeyError):
        context = {'album': album, 'error_message': 'You want to do what?'}
        return render(request, 'music/album.html', context)


class AlbumCreate(CreateView):

    model = Album
    fields = [
        'album_title',
        'artist',
        'genre',
        'album_logo'
    ]


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class AlbumUpdate(UpdateView):
    model = Album
    fields = [
        'album_title',
        'artist',
        'genre',
        'album_logo'
    ]



