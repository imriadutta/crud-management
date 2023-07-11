from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.models import *
from .serializers import *
# from django.contrib.admin.views.decorators import staff_member_required
from myapp.group import EachGroup
from django.shortcuts import redirect


# @staff_member_required(login_url='/login')
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, uname):
    try:
        user = User.objects.get(username=uname)
    except Exception:
        return redirect('/api/users')
    else:
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def setUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteUser(request, uname):
    try:
        user = User.objects.get(username=uname)
    except Exception:
        return redirect('/api/users')
    else:
        user.delete()
        return Response('User deleted successfully.')


@api_view(['PUT'])
def updateUser(request, uname):
    try:
        user = User.objects.get(username=uname)
    except Exception:
        return redirect('/api/users')
    else:
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def getGroups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getGroup(request, gname):
    try:
        group = Group.objects.get(name=gname)
    except Exception:
        return redirect('/api/groups')
    else:
        serializer = GroupSerializer(group)
        return Response(serializer.data)


@api_view(['POST'])
def setGroup(request):
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteGroup(request, gname):
    try:
        group = Group.objects.get(name=gname)
    except Exception:
        return redirect('/api/groups')
    else:
        group.delete()
        return Response('Group deleted successfully.')


@api_view(['PUT'])
def updateGroup(request, gname):
    try:
        group = Group.objects.get(name=gname)
    except Exception:
        return redirect('/api/groups')
    else:
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
