from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
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
        instance.username = validated_data.get(
            None, instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()

        for key, value in profile_data.items():
            if(key == 'owner_assigned'):
                profile.owner_assigned.set(value)
            elif(key == 'short_name'):
                profile.short_name = value
            profile.save()
            print(key, value)
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
