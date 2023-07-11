from rest_framework import serializers
from myapp.models import *


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    # members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'admin')


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'phone')
