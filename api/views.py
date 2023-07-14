from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.models import *
from .serializers import *
from myapp.group import EachGroup
from django.shortcuts import redirect


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


@csrf_exempt
def getdata(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = []

        for user in users:
            members = Member.objects.filter(user=user)
            context = {
                'username': user.username,
                'groups': [m.group.name for m in members]
            }
            data.append(context)

        return JsonResponse(data, safe=False)


@csrf_exempt
def setData(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        username = request_data.get('username')
        groupnames = request_data.get('groups')
        if username and groupnames:
            context = {
                'username': username,
                'groups': groupnames
            }
            try:
                user = User.objects.get(username=username)
                groups = []
                for groupname in groupnames:
                    groups += Group.objects.filter(name=groupname)
            except Exception:
                pass
            else:
                for group in groups:
                    member = Member.objects.create(
                        group=group,
                        user=user
                    )
                    member.save()
                data = {
                    'message': 'Successfully added',
                    'data': context
                }
                return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Invalid data'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def removeData(request):
    if request.method == 'DELETE':
        request_data = json.loads(request.body)
        username = request_data.get('username')
        groupnames = request_data.get('groups')
        if username and groupnames:
            try:
                user = User.objects.get(username=username)
                groups = []
                for groupname in groupnames:
                    groups += Group.objects.filter(name=groupname)
            except Exception:
                pass
            else:
                for group in groups:
                    member = Member.objects.filter(
                        group=group,
                        user=user
                    )
                    member.delete()
                data = {
                    'message': 'Successfully removed'
                }
                return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Invalid data'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)
