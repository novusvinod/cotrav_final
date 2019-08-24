from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'API_BASE_URL': settings.API_BASE_URL
    }