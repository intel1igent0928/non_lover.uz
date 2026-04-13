from rest_framework import serializers
from .models import Banner, StoryCategory, StoryItem, SiteContent, CourseFeature, SplashLink, SocialLink

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class StoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryItem
        fields = ['image', 'order']

class StoryCategorySerializer(serializers.ModelSerializer):
    items = StoryItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StoryCategory
        fields = ['name', 'label', 'thumbnail', 'items', 'order']

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ['key', 'value']

class CourseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeature
        fields = '__all__'

class SplashLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplashLink
        fields = '__all__'

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
