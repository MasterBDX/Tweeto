from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def get_first_name(self, obj):
        return obj.username

    def get_avatar(self, obj):
        try:
            avatar = obj.profile.avatar.url
        except:
            avatar = None
        return avatar
