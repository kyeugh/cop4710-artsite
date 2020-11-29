from django import template

register = template.Library()

@register.filter
def liked_by(artwork, user):
    return artwork.votes.filter(id=user.id).exists()