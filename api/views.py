from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from image.models import ImagePost
from api.serializers import ImageSerializer


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
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
    account = request.user

    image_post = ImagePost(author=account)

    if request.method == "POST":
        serializer = ImageSerializer(image_post, context={'request': request}, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
