"""kreedo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

admin.site.site_header = "Kreedo Administration"
admin.site.site_title = "Kreedo Admin Portal"
admin.site.index_title = "Welcome to Kreedo Admin Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.api.urls')),
    path('school/', include('schools.api.urls')),
    path('session/', include('session.api.urls')),
    path('plan/', include('plan.api.urls')),
    path('holiday/', include('holiday.api.urls')),
    path('package/', include('package.api.urls')),
    path('activity/', include('activity.api.urls')),
    path('material/', include('material.api.urls')),
    path('area_of_devlopment/', include('area_of_devlopment.api.urls')),
    path('period/', include('period.api.urls')),
    path('child/', include('child.api.urls')),
    path('group/', include('group.api.urls')),




]


# Debugger toolbar setting

if settings.DEBUG:
    import debug_toolbar
    import traceback
    try:
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except Exception as ex:
        print(traceback.print_exc())
