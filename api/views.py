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
from sorl.thumbnail import get_thumbnail

CREATE_SUCCESS = 'created'


def share_link(request, image):
    """
    Function to share a link
    request: request, image: model.<image>
    """
    image_url = str(request.build_absolute_uri(image.url))
    if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
    return image_url


def get_thumbnail_200(image):
    thumbnail_200 = get_thumbnail(image, '200x200', crop='center', quality=60)

    return thumbnail_200


def get_thumbnail_400(image):
    thumbnail_400 = get_thumbnail(image, '400x400', crop='center', quality=60)

    return thumbnail_400

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


# TODO: Add token expires in time
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_image_view(request):
    global thumbnail_widgh, thumbnail_height, original_file
    if request.method == 'POST':
        data = request.data
        data['author'] = request.user.pk
        serializer = ImagePostCreateSerializer(data=data)
        account_tier = str(request.user.account_tier)
        print(account_tier)
        data = {}

        if serializer.is_valid():
            image_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['slug'] = image_post.slug
            data['username'] = image_post.author.username

            # Basic account
            if account_tier == 'Basic':
                thumbnail_200 = get_thumbnail_200(image_post.image)
                data['image_thumbnail_200'] = share_link(request, thumbnail_200)

            # Premium account
            elif account_tier == 'Premium':
                thumbnail_200 = get_thumbnail_200(image_post.image)
                data['image_thumbnail_200'] = share_link(request, thumbnail_200)

                thumbnail_400 = get_thumbnail_400(image_post.image)
                data['image_thumbnail_400'] = share_link(request, thumbnail_400)

                data['original_link'] = share_link(request, image_post.image)

            # Enterprise account
            elif account_tier == 'Enterprise':
                thumbnail_200 = get_thumbnail_200(image_post.image)
                data['image_thumbnail_200'] = share_link(request, thumbnail_200)

                thumbnail_400 = get_thumbnail_400(image_post.image)
                data['image_thumbnail_400'] = share_link(request, thumbnail_400)

                data['original_link'] = share_link(request, image_post.image)

            # Account plans created by admin
            elif account_tier not in ('Basic', 'Premium', 'Enterprise'):
                query_results = Plan.objects.filter(plan_name=account_tier)

                for query_result in query_results:
                    thumbnail_widgh = query_result.thumbnail_width
                    thumbnail_height = query_result.thumbnail_height
                    original_file = query_result.original_file
                    expires_link = query_result.expires_link

                size = str(thumbnail_widgh) + 'x' + str(thumbnail_height)
                thumbnail = get_thumbnail(image_post.image, size, crop='center', quality=60)
                data['image_thumbnail'] = share_link(request, thumbnail)

                if original_file is True:
                    data['original_link'] = share_link(request, image_post.image)

                if expires_link is True:
                    pass

            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
