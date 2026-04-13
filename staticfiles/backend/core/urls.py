from django.urls import path
from .views import SiteContentView, GalleryView, SplashLinksView

urlpatterns = [
    path('content/', SiteContentView.as_view(), name='site-content'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('splash-links/', SplashLinksView.as_view(), name='splash-links'),
]
