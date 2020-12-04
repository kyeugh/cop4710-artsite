from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST

from django.views.generic.detail import DetailView

from art_app.forms import RegistrationForm, ArtworkForm, CollectionForm
from art_app.models import *
from django.db.models import F, Count


# Create your views here.
def index(request):
    latest = Artwork.objects.all().order_by('-created')[:10]
    today = Artwork.objects.filter(
        created__gte=timezone.now().replace(
            hour=0, minute=0, second=0
        )
    ).all()
    hot = sorted(today, key=lambda t: t.total_votes, reverse=True)[:10]
    if request.user.is_authenticated:
        user_collections = Collection.objects.filter(artist=request.user)
    else:
        user_collections = None
    return render(request, 'home.html', {"latest": latest, "hot": hot, "user_collections": user_collections})


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
            artwork.save()

            raw_tags = form.cleaned_data["tags"]
            tags = raw_tags.split(",")
            tags = [tag.lower() for tag in tags]
            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
            artwork.tags.add(*tags)
            artwork.votes.add(request.user)
            artwork.save()

            return redirect("home")
    else:
        form = ArtworkForm()
    return render(request, "upload.html", {"form": form})


@login_required
def new_collection(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.name = form.cleaned_data.get("name")
            collection.artist = request.user
            collection.save()

            raw_tags = form.cleaned_data["tags"]
            tags = raw_tags.split(",")
            tags = [tag.lower() for tag in tags]
            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
            collection.tags.add(*tags)

            collection.save()

            return redirect("/collections/" + collection.slug)

    else:
        form = CollectionForm()
    return render(request, "create-collection.html", {"form": form})


def explore(request):
    tags = Tag.objects.all()
    # return render(request, 'home.html', {"latest": latest})
    return render(request, "explore.html", {"tags": tags})


@login_required
@require_POST
def vote(request):
    if request.method == "POST":
        user = request.user
        slug = request.POST.get("slug", None)
        artwork = get_object_or_404(Artwork, slug=slug)

        if artwork.votes.filter(id=user.id).exists():
            artwork.votes.remove(user)
            message = "You unliked the post."
        else:
            artwork.votes.add(user)
            message = "You liked the post."

    ctx = {"votes_count": artwork.total_votes, "message": message}
    return HttpResponse(json.dumps(ctx), content_type="application/json")


@login_required
@require_POST
def save(request):
    ctx = {"added": False}
    if request.method == "POST":
        artwork_slug = request.POST.get("artwork-slug", None)
        collection_slug = request.POST.get("collection-slug", None)
        artwork = get_object_or_404(Artwork, slug=artwork_slug)
        collection = get_object_or_404(Collection, slug=collection_slug)
        if artwork not in collection.artworks.all():
            collection.artworks.add(artwork)
            ctx["added"] = collection.get_absolute_url()
        collection.save()
    return HttpResponse(json.dumps(ctx), content_type="application/json")

def collections(request):
    all_collections = Collection.objects.all()
    return render(request, "collections.html", {"collections": all_collections})

def search(request):
    query = request.GET.get("q")
    artworks = Artwork.objects.filter(title__icontains=query)
    artists = Artist.objects.filter(username__icontains=query)
    collections = Collection.objects.filter(name__icontains=query)
    tags = Tag.objects.filter(name__icontains=query)
    return render(request, "search.html", {"artworks": artworks, "artists": artists, "collections": collections, "tags": tags})

def contest(request):
    contestName = "paint"
    tagId = Tag.objects.get(name=contestName)
    artworks = Artwork.objects.filter(
        tags__in=[tagId]).order_by('-votes')[:10]
    artworks[0].votes.count()
    return render(request, "contest.html", {"artworks": artworks, "contestName": contestName})


def leaderboard(request):
    # need to order artists by the number of votes that they got
    topArtists = sorted(Artist.objects.all(), key=lambda t: t.total_votes, reverse=True)
    return render(request, "leaderboard.html", {"artists": topArtists})


@login_required
def CreateCollection(request):
    collections = Collection.objects.all()
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.name = form.cleaned_data.get("name")
            collection.artist = request.user
            collection.save()

            return redirect("collections")

    else:
        form = CollectionForm()
    return render(request, "collections.html", {"form": form, "collections": collections})


def leaderboard(request):
    # need to order artists by the number of votes that they got
    artists = Artist.objects.all()  # .order_by('-votes')[:10]
    return render(request, "leaderboard.html", {"artists": artists})


@login_required
def CreateCollection(request):
    collections = Collection.objects.all()
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.name = form.cleaned_data.get("name")
            collection.artist = request.user
            collection.save()

            return redirect("collections")

    else:
        form = CollectionForm()
    return render(request, "collections.html", {"form": form, "collections": collections})

#tiffany
@login_required
def delete_art(request, pk):
     Artwork.objects.filter(id=pk).delete()

     items = Artwork.objects.all()

     context = {
        "items": items
     }

     return render(request, "artwork_detail.html", context)

class ArtworkDetailView(DetailView):
    model = Artwork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_collections"] = Collection.objects.filter(
                artist=self.request.user)
        return context


class CollectionDetailView(DetailView):
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artworks"] = get_object_or_404(
            Collection, slug=context["collection"].slug).artworks.all()
        return context


class ArtistDetailView(DetailView):
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artworks"] = Artwork.objects.filter(artist=context["artist"])
        context["collections"] = Collection.objects.filter(
            artist=context["artist"])
        return context


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artworks"] = Artwork.objects.filter(tags__in=[context["tag"]])
        return context
