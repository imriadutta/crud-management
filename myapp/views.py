from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.contrib.auth import login as signin, logout as signout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .group import EachGroup


@login_required(login_url='/login')
def dashboard(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'dashboard.html', context)


def login(request):
    if request.session.get('username'):
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).last()
        if user and (user.password == password or check_password(password, user.password)):
            request.session['username'] = user.username
            request.session['user_is_staff'] = user.is_staff
            signin(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 f'Successfully logged in. Welcome {user.fullname} !')
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            else:
                return redirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Wrong Username or Password.')
    return render(request, 'login.html')


@login_required(login_url='/login')
def logout(request):
    request.session['username'] = ''
    request.session['user_is_staff'] = False
    signout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out.')
    return redirect('/login')


@login_required(login_url='/login')
def profile(request, uname):
    try:
        user = User.objects.get(username=uname)
    except Exception:
        messages.add_message(request, messages.ERROR, 'User does not exist!')
        return redirect('/')
    else:
        if request.method == 'POST':
            user.email = request.POST.get('email')
            user.fullname = request.POST.get('fullname')
            if request.FILES.get('profile-picture'):
                user.profile_picture = request.FILES.get('profile-picture')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            user.password = request.POST.get('password')
            if request.POST.get('gender'):
                user.gender = request.POST.get('gender')
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'User details changed successfully.')
            return redirect('/')

        return render(request, 'profile.html', {'user': user})


@login_required(login_url='/login')
def profile_delete(request, uname):
    try:
        user = User.objects.get(username=uname)
    except Exception:
        messages.add_message(request, messages.ERROR, 'User does not exist!')
    else:
        messages.add_message(request, messages.SUCCESS,
                             'User deleted successfully.')
        if request.session.get('user_is_staff'):
            user.delete()
        else:
            signout(request)
            user.delete()
            request.session['username'] = ''
            request.session['user_is_staff'] = False
            return redirect('/login')
    finally:
        return redirect('/')


@login_required(login_url='/login')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        profile_picture = request.FILES.get('profile-picture')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        gender = request.POST.get('gender')
        user = User.objects.filter(username=username).last()

        if user:
            messages.add_message(request, messages.WARNING,
                                 'User already exists!')
        else:
            if password == cpassword:
                user = User.objects.create(
                    username=username,
                    email=email,
                    fullname=fullname,
                    password=password,
                    address=address,
                    phone=phone,
                    gender=gender,
                )
                user.save()
                user.profile_picture = profile_picture
                user.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Successfully user created.')
                return redirect('/')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Password does not match!')
    return render(request, 'register.html')


@login_required(login_url='/login')
def create_group(request):
    myuser = User.objects.get(username=request.session.get('username'))
    users = User.objects.all()

    if request.method == 'POST':
        name = request.POST.get('gname')
        if Group.objects.filter(name=name):
            messages.add_message(
                request, messages.ERROR, 'Group name already exists!')
        else:
            admin = myuser
            group = Group.objects.create(
                name=name,
                admin=admin,
            )
            group.save()

            member = Member.objects.create(
                group=group,
                user=myuser,
            )
            member.save()
            for user in users:
                if request.POST.get(user.username):
                    member = Member.objects.create(
                        group=group,
                        user=user,
                    )
                    member.save()

            messages.add_message(
                request, messages.SUCCESS, 'Successfully group created.')
            return redirect('/groups')

    context = {
        'myuser': myuser,
        'users': users,
    }
    return render(request, 'create-group.html', context)


@login_required(login_url='/login')
def show_groups(request):
    groups = Group.objects.all()

    allgroups = []
    for group in groups:
        eachgroup = EachGroup(
            name=group.name,
            admin=group.admin,
            created_on=group.created_on,
            modified_on=group.modified_on
        )
        eachgroup.members = Member.objects.filter(group=group)
        allgroups.append(eachgroup)

    context = {
        'groups': allgroups,
    }
    return render(request, 'groups.html', context)


@login_required(login_url='/login')
def group_delete(request, gname):
    try:
        group = Group.objects.get(name=gname)
    except Exception:
        messages.add_message(request, messages.ERROR, 'Group does not exist!')
    else:
        messages.add_message(request, messages.SUCCESS,
                             'Group deleted successfully.')
        group.delete()
    finally:
        return redirect('/groups')


@login_required(login_url='/login')
def group_edit(request, gname):
    try:
        group = Group.objects.get(name=gname)
        eachgroup = EachGroup(
            name=group.name,
            admin=group.admin,
            created_on=group.created_on,
            modified_on=group.modified_on
        )
        eachgroup.members = [
            m.user for m in Member.objects.filter(group=group)
        ]
    except Exception:
        messages.add_message(request, messages.ERROR, 'Group does not exist!')
        return redirect('/groups')
    else:
        if request.method == 'POST':
            name = request.POST.get('gname')
            if Group.objects.filter(name=name).exclude(name=group.name):
                messages.add_message(
                    request, messages.WARNING, 'Group name already exists!')
            else:
                group.name = name
                members = Member.objects.filter(group=group)
                members.delete()

                myuser = User.objects.get(
                    username=request.session.get('username'))
                users = User.objects.all()

                member = Member.objects.create(
                    group=group,
                    user=myuser,
                )
                member.save()
                for user in users:
                    if request.POST.get(user.username):
                        member = Member.objects.create(
                            group=group,
                            user=user,
                        )
                        member.save()
                group.save()

                messages.add_message(request, messages.SUCCESS,
                                     'Group details saved successfully.')
                return redirect('/groups')

        context = {
            'group': eachgroup,
            'users': User.objects.all(),
        }
        return render(request, 'each-group.html', context)
