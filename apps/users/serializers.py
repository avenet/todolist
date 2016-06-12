from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email',
                  'first_name',
                  'last_name')
