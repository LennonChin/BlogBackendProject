from django.shortcuts import render
from django.views.generic.base import View

from base.models import SiteInfo


class IndexView(View):
    def get(self, request):
        site_infos = SiteInfo.objects.all().filter(is_live=True)[0]
        context = {
            'site_infos': site_infos
        }
        return render(request, 'index.html', context)
