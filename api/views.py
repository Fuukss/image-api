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
from api.serializers import ImageSerializer


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


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_image_view(request):
    """
    This view should post a image
    for the currently authenticated user
    and response details.
    """
    account = request.user

    image_post = ImagePost(author=account)

    if request.method == "POST":
        serializer = ImageSerializer(image_post, context={'request': request}, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
