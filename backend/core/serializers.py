from rest_framework import serializers
from .models import SiteContent, StoryCategory, StoryItem, SplashLink

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ['key', 'value']

class StoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryItem
        fields = ['image', 'order']

class StoryCategorySerializer(serializers.ModelSerializer):
    items = StoryItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StoryCategory
        fields = ['name', 'label', 'thumbnail', 'items', 'order']

class SplashLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplashLink
        fields = ['title', 'url', 'icon_type', 'order']
