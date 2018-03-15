from django.shortcuts import render
from django.views.generic.base import View

from user.models import GuestProfile
from BlogBackendProject.settings import SITE_BASE_URL


# Create your views here.


class SubscribeView(View):
    def get(self, request):
        guest = GuestProfile.objects.filter(uuid=request.GET.get('id'))[0]
        if guest:
            guest.is_subcribe = True
            guest.save()
            context = {
                'base_url': SITE_BASE_URL,
                'message': '您已成功订阅评论相关的邮件',
                'unsubscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'unsubscribe', guest.uuid),
                'subscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'subscribe', guest.uuid),
            }
            return render(request, 'Subscribe.html', context)
        else:
            context = {
                'base_url': SITE_BASE_URL,
                'error': '操作出错，请重试'
            }
            return render(request, 'Subscribe.html', context)


class UnSubscribeView(View):
    def get(self, request):
        guest = GuestProfile.objects.filter(uuid=request.GET.get('id'))[0]
        if guest:
            guest.is_subcribe = False
            guest.save()
            context = {
                'base_url': SITE_BASE_URL,
                'message': '您已成功取消订阅评论相关的邮件',
                'unsubscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'unsubscribe', guest.uuid),
                'subscribe_url': '{0}/{1}/?id={2}'.format(SITE_BASE_URL, 'subscribe', guest.uuid),
            }
            return render(request, 'UnSubscribe.html', context)
        else:
            context = {
                'base_url': SITE_BASE_URL,
                'error': '操作出错，请重试'
            }
            return render(request, 'UnSubscribe.html', context)
