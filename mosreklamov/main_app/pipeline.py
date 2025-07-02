import requests
from django.core.files.base import ContentFile

def save_avatar(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        avatar_url = response.get('avatar_url')
        if avatar_url:
            avatar_response = requests.get(avatar_url)
            if avatar_response.status_code == 200:
                user.photo.save(
                    f'{user.username}_github.jpg',
                    ContentFile(avatar_response.content),
                    save=True
                )