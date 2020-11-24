from django.contrib import admin
from django.apps import apps

app = apps.get_app_config("art_app")

class ArtworkAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ArtistAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(app.models["artwork"], ArtworkAdmin)
admin.site.register(app.models["artist"], ArtistAdmin)

for name, model in app.models.items():
    if name not in ["artwork", "artist"]:
        admin.site.register(model)