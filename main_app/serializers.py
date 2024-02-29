from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import  Item, Swap, Profile, Photo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'id']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['url']

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['item_title', 'item_description', 'listing_active', 'user', 'id', 'image']

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        item = Item.objects.create(**validated_data)
        if image_file:
            item.image.save(image_file.name, image_file, save=True)

        return item

class SwapSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source='item',  # This tells DRF which model attribute to map this field to
        write_only=True  # This field is used for writing an item ID upon creation but not included in serialization output
    )

    class Meta:
        model = Swap
        fields = ['item_title', 'item_description', 'offer_accepted', 'item_id', 'user']

# class SwapSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Swap
#         fields = ['item_title', 'item_description', 'offer_accepted', 'item_id']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['user']


