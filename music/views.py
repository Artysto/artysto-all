from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
#from django.shortcuts import redirect

# Create your views here.


def base(request):
    """ Renders just the template for nav bar not user accesible """
    return render(request, 'music/base.html', context={})


def index(request):
    """ Renders /music/ """
    all_album = Album.objects.all()
    query = request.GET.get('q')
    if query:
        all_album = all_album.filter(Q(album_title__icontains=query) | Q(artist__icontains=query))
    return render(request, 'music/index.html', context={'all_album': all_album, 'query': query })


def artists(request):
    """ Renders /music/artists deprecated """

    html = "<h1> This page is a listing of all artists that you can discover on this site<h1>"
    all_album = Album.objects.all()
    for album in all_album:
        html += "<li>" + album.artist + "</li>"

    return HttpResponse(html)


def albums(request):
    """ Renders /music/albums deprecated """

    html = "<h1> This page is a listing of all albums that you can discover on this site<h1>"
    all_album = Album.objects.all()
    for album in all_album:
        html += "<li>" + "<a href ='/music/" + str(album.id) + "' >" + album.album_title + "</a>" + "</li>"

    return HttpResponse(html)


def album_id(request, ids):
    """ Renders /music/<id> for albums """

    try:
        context = {'album': Album.objects.filter(id=ids)[0]}
        return render(request, 'music/album.html', context)
    except IndexError:
        raise Http404("What you are looking for doesn't even exist. How did you even get here? Don't drink and type")


def songs(request):
    """ Renders /music/songs """

    all_albums = Album.objects.all()
    all_songs =[]
    query = request.GET.get('q')

    for album in all_albums:
        songs_queryset = Song.objects.filter(album=album.id) 
        if query:
            all_songs += songs_queryset.filter(song_title__icontains=query)
        else:
            all_songs += songs_queryset
    
    if query:
        albums = Album.objects.filter(Q(album_title__icontains=query) | Q(artist__icontains=query))
        for album in albums:
            all_songs += album.song_set.all()

    return render(request, 'music/songs.html', context={'song_list': list(set(all_songs)), 'query': query})


class SongCreate(CreateView):
    """ Renders /music/<album-id>/add-songs """

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
    """ Deprecated implementation for song delete """

    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/album.html', {'album': album})


def favourite(request, ids):
    """ Responds to /music/<album-id>/favourite """
  
    selected_song = get_object_or_404(Song, id=ids)
    try:
        #selected_song = album.song_set.get(id=request.POST['song'])
        selected_song.is_favorite = not selected_song.is_favorite
        selected_song.save()
        #context = {'album': album}
        #return render(request, 'music/album.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except (IndexError, KeyError):
        context = {'album': album, 'error_message': 'You want to do what?'}
        return render(request, 'music/album.html', context)


class AlbumCreate(CreateView):
    """ Renders /music/add-album """

    model = Album
    fields = [
        'album_title',
        'artist',
        'genre',
        'album_logo'
    ]


class AlbumDelete(DeleteView):
    """ Renders /music/<album-id>/delete """

    model = Album
    success_url = reverse_lazy('music:index')


class AlbumUpdate(UpdateView):
    """ Renders /music/<album-id>/update-album """

    model = Album
    fields = [
        'album_title',
        'artist',
        'genre',
        'album_logo'
    ]



