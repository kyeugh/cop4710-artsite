from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import DetailView

from art_app.forms import RegistrationForm, ArtworkForm
from art_app.models import *
from django.db.models import F


# Create your views here.
def index(request):
    # if request.method == 'POST' and 'increment_votes' in request.POST:
    #    Artwork.objects.all().filter(id__in=F(1)).update(votes=F('votes') + 1)
    latest = Artwork.objects.all().order_by('-votes')[:10]

    return render(request, 'home.html', {"latest": latest})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def new_artwork(request):
    from .models import Tag
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user
            artwork.votes = 0
            artwork.save()

            raw_tags = form.cleaned_data["tags"]
            tags = raw_tags.split(",")
            tags = [tag.lower() for tag in tags]
            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
            print(tags)
            artwork.tags.add(*tags)
            artwork.save()

            return redirect("home")
    else:
        form = ArtworkForm()
    return render(request, "upload.html", {"form": form})


def explore(request):
    tags = Tag.objects.all()
    # return render(request, 'home.html', {"latest": latest})
    return render(request, "explore.html", {"tags": tags})


# def vote(artId):
 #   Artwork.objects.filter(id__in=artId).update(votes=F('votes') + 1)


class ArtworkDetailView(DetailView):
    model = Artwork


class ArtistDetailView(DetailView):
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artworks"] = Artwork.objects.filter(artist=context["artist"])
        return context


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artworks"] = Artwork.objects.filter(tags__in=[context["tag"]])
        return context
