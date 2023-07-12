from django.urls import path
from .views import *

urlpatterns = [
    path('', getdata),
    path('add', setData),
    path('remove', removeData),

    path('users', getUsers),
    path('user/<str:uname>', getUser),
    path('users/add', setUser),
    path('user/update/<str:uname>', updateUser),
    path('user/delete/<str:uname>', deleteUser),

    path('groups', getGroups),
    path('group/<str:gname>', getGroup),
    path('groups/add', setGroup),
    path('group/update/<str:gname>', updateGroup),
    path('group/delete/<str:gname>', deleteGroup),
]
