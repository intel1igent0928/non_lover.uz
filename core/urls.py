from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BannerViewSet, StoryCategoryViewSet, StoryItemViewSet,
    SiteContentViewSet, CourseFeatureViewSet, 
    SplashLinkViewSet, SocialLinkViewSet
)

router = DefaultRouter()
router.register(r'banner', BannerViewSet)
router.register(r'gallery', StoryCategoryViewSet)
router.register(r'story-item', StoryItemViewSet)
router.register(r'content', SiteContentViewSet)
router.register(r'features', CourseFeatureViewSet)
router.register(r'splash-links', SplashLinkViewSet)
router.register(r'social-links', SocialLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
