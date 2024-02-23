from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import  Item, Swap, Profile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['item_title', 'item_description', 'listing_active']

class SwapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Swap
        fields = ['item_title', 'item_description', 'offer_accepted']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['user']

