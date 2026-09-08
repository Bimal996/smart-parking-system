from django.conf import settings


def site_settings(request):
    """Make the global SPS settings dict available in every template as `site`."""
    return {"site": settings.SPS_SETTINGS}
