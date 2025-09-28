from rest_framework import serializers
from users.models import UsersData
# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UsersData
        fields = ['url', 'username', 'email', 'is_staff']
