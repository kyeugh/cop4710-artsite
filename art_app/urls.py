from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("new/artwork", views.new_artwork, name="upload"),
    path('art/<slug:slug>', views.ArtworkDetailView.as_view(), name='artwork-detail'),
    path("artists/<slug:slug>",
         views.ArtistDetailView.as_view(), name='artist-detail'),
    path("tags/<slug:slug>", views.TagDetailView.as_view(), name="tag-detail"),
    path("collections/<slug:slug>", views.CollectionDetailView.as_view(), name="collection-detail"),
    path("explore", views.explore, name="explore"),
    path("contest", views.contest, name="contest"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("vote", views.vote, name="vote"),
    path("save", views.save, name="save"),
    path("new/collection", views.new_collection, name="new-collection")
    path("delete", views.delete_art, name="delete-art")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
