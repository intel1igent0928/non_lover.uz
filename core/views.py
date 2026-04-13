from rest_framework import viewsets
from rest_framework.response import Response
from .models import Banner, StoryCategory, SiteContent, CourseFeature, SplashLink, SocialLink
from .serializers import (
    BannerSerializer, StoryCategorySerializer, 
    SiteContentSerializer, CourseFeatureSerializer, 
    SplashLinkSerializer, SocialLinkSerializer
)

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class StoryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoryCategory.objects.all().prefetch_related('items')
    serializer_class = StoryCategorySerializer

class SiteContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer

    def list(self, request):
        queryset = self.get_queryset()
        data = {item.key: item.value for item in queryset}
        return Response(data)

class CourseFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseFeature.objects.all()
    serializer_class = CourseFeatureSerializer

class SplashLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SplashLink.objects.all()
    serializer_class = SplashLinkSerializer

class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
