from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from image.models import ImagePost
from plan.model import Plan
from api.serializers import ImageSerializer, ImagePostCreateSerializer


@permission_classes((IsAuthenticated,))
class ApiImageListView(generics.ListAPIView):
    """
    Url: https://<your-domain>/api/blog/list
    Headers: Authorization: Token <token>

    Return a list of of all the images
    for the currently authenticated user.
    """
    queryset = ImagePost.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return ImagePost.objects.filter(author=user)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_image_view(request):
    """
    Url: https://<your-domain>/api/image/create
    Headers: Authorization: Token <token>
    Body: image: image file in png or jpg format and file size less than 2Mb
    """
    if request.method == 'POST':
        data = request.data
        data['author'] = request.user.pk
        serializer = ImagePostCreateSerializer(data=data)
        account_tier = str(request.user.get_account_tier())
        data = {}

        if serializer.is_valid():
            image_post = serializer.save()
            user_plan = Plan.objects.filter(plan_name=account_tier)

            for available_thumbnails in user_plan:
                available_sizes = available_thumbnails.get_thumbnail_plan()
                original_file = available_thumbnails.get_original_file()
                expires_image = available_thumbnails.get_expires_link()

                for available_size in available_sizes:
                    data[available_size] = image_post.get_a_thumbnail(request, available_size)

                if original_file is True:
                    data['original image:'] = image_post.get_original_image(request)

                if expires_image is True:
                    data['expires image'] = image_post.get_original_expires_image(request)

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
