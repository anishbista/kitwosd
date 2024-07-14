from mainapp.models import SiteSettings


def base_context(request):
    site_info = SiteSettings.objects.first() or None

    return {
        "site_info": site_info,
    }
