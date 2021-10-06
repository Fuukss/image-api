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
                data['image_thumbnail_200'] = share_link(request, image_post.image_thumbnail_200)

            # Premium account
            elif account_tier == 'Premium':
                data['image_thumbnail_200'] = share_link(request, image_post.image_thumbnail_200)
                data['image_thumbnail_400'] = share_link(request, image_post.image_thumbnail_400)
                data['original_link'] = share_link(request, image_post.image)

            # Enterprise account
            elif account_tier == 'Enterprise':
                data['image_thumbnail_200'] = share_link(request, image_post.image_thumbnail_200)
                data['image_thumbnail_400'] = share_link(request, image_post.image_thumbnail_400)
                data['original_link'] = share_link(request, image_post.image)

            elif account_tier not in ('Basic', 'Premium', 'Enterprise'):
                query_results = Plan.objects.filter(plan_name=account_tier)
                for query_result in query_results:
                    thumbnail_widgh = query_result.thumbnail_width
                    thumbnail_height = query_result.thumbnail_height
                    original_file = query_result.original_file
                    expires_link = query_result.expires_link

            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
