"""firstdrf URL Configuration

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register('main', views.MainViewSet)
# router.register('cse', views.CseViewSet)

# ViewSet에 필요한 url 자동 등록
for name, cls in views.__dict__.items():
    idx = name.find('ViewSet')
    if idx != -1:
        router.register(name[:idx].lower(), cls)

urlpatterns = [
    path('', include(router.urls)),
    path(r'list/', views.get_board_list, name='get_board_list'),
    path(r'all', views.get_board_all, name='get_board_all'),
]
