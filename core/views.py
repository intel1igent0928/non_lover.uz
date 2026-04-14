from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Banner, StoryCategory, StoryItem, SiteContent, CourseFeature, SplashLink, SocialLink
from .serializers import (
    BannerSerializer, StoryCategorySerializer, StoryItemSerializer,
    SiteContentSerializer, CourseFeatureSerializer, 
    SplashLinkSerializer, SocialLinkSerializer
)

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class StoryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StoryCategory.objects.all().prefetch_related('items')
    serializer_class = StoryCategorySerializer

from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class StoryItemViewSet(viewsets.GenericViewSet):
    queryset = StoryItem.objects.all()
    serializer_class = StoryItemSerializer
    authentication_classes = [] # Disable CSRF check by disabling session authentication
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        item = self.get_object()
        item.likes += 1
        item.save()
        return Response({'status': 'liked', 'likes': item.likes})

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        item = self.get_object()
        item.shares += 1
        item.save()
        return Response({'status': 'shared', 'shares': item.shares})

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
