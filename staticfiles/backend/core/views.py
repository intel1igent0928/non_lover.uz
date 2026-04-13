from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteContent, StoryCategory, SplashLink
from .serializers import SiteContentSerializer, StoryCategorySerializer, SplashLinkSerializer

class SiteContentView(APIView):
    def get(self, request):
        content = SiteContent.objects.all()
        serializer = SiteContentSerializer(content, many=True)
        # Convert to key-value dict for easier frontend use
        data = {item['key']: item['value'] for item in serializer.data}
        return Response(data)

class GalleryView(APIView):
    def get(self, request):
        categories = StoryCategory.objects.all()
        serializer = StoryCategorySerializer(categories, many=True)
        return Response(serializer.data)

class SplashLinksView(APIView):
    def get(self, request):
        links = SplashLink.objects.all()
        serializer = SplashLinkSerializer(links, many=True)
        return Response(serializer.data)
