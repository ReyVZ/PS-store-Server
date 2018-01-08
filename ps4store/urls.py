"""ps4store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import mainapp.views as mainapp
import adminapp.views as adminapp
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
    

urlpatterns = [    
    url(r'^$', mainapp.main, name='main'),
    url(r'^catalog/page/(?P<page>\d+)/$', mainapp.catalog, name='catalog'),
    url(r'^contacts/', mainapp.contacts, name='contacts'),
    url(r'^driveclub/', mainapp.driveclub, name='driveclub'),
    # url(r'^user/login/$', mainapp.login, name='login'),
    # url(r'^user/logout/$', mainapp.logout, name='logout'),
    # url(r'^user/registration/$', mainapp.registration, name='registration'),
    url(r'^admin/', include('adminapp.urls', namespace='admin')),
    url(r'^auth/', include('authapp.urls', namespace='auth'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

