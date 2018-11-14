import logging
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger('blog.views')

def global_setting(request):
  return {   'SITE_NAME' : settings.SITE_NAME,
             'SITE_DESC': settings.SITE_DESC,
             'WEIBO_SINA': settings.WEIBO_SINA,
             'WEIBO_TENCENT': settings.WEIBO_TENCENT,
             'PRO_RSS': settings.PRO_RSS,
             'PRO_EMAIL': settings.PRO_EMAIL,
  }




# Create your views here.
def index(request):
  try:
    file =open('ass.txt','r')
  except Exception as e:
    logger.error(e)
  return render(request, 'index.html',locals())


