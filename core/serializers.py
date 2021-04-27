from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfileModel


# class CustomerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'is_superuser']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileModel
        fields = ['owner_assigned', 'short_name']


class UserSerializer(serializers.ModelSerializer):
    # profile_set = serializers.PrimaryKeyRelatedField(many=True)
    # profile = UserProfileSerializer(many=True, source='owner_assigned')

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'date_joined', 'last_login', 'is_active', 'profile']
        depth = 1

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        # User
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.username = validated_data.get(
            'username', instance.username)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()

        # Profile
        profile.owner_assigned.set(profile_data['owner_assigned'])
        profile.short_name = profile_data.get(
            'short_name', profile.short_name)
        profile.save()

        return instance

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)

        profile = user.profile
        profile.owner_assigned.set(profile_data['owner_assigned'])
        profile.short_name = profile_data.get(
            'short_name', profile.short_name)
        profile.save()
        return user
