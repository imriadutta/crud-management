
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('profile/<str:uname>', profile),
    path('profile-delete/<str:uname>', profile_delete),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('create-group', create_group),
    path('groups', show_groups),
    path('group-delete/<str:gname>', group_delete),
    path('group/<str:gname>', group_edit),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
