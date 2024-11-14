from .models import SiteInfo

def site_info(request):
    site_info = SiteInfo.objects.first()
    return {'site_info': site_info}