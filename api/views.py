from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework import generics

from account.models import Account
from image.models import ImagePost
from api.serializers import ImageSerializer, ImagePostCreateSerializer

CREATE_SUCCESS = 'created'


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_image_view(request, slug):
    try:
        image_post = ImagePost.objects.get(slug=slug)
    except ImagePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ImageSerializer(image_post, context={'request': request})
        return Response(serializer.data)

# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
@permission_classes((IsAuthenticated,))
class ApiImageListView(generics.ListAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        This view should return a list of all the images
        for the currently authenticated user.
        """
        user = self.request.user
        return ImagePost.objects.filter(author=user)


# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_image_view(request):
    if request.method == 'POST':

        data = request.data
        data['author'] = request.user.pk
        serializer = ImagePostCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            image_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['slug'] = image_post.slug
            image_url = str(request.build_absolute_uri(image_post.image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['image'] = image_url
            data['username'] = image_post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
