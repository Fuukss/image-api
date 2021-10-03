from rest_framework import serializers

from image.models import ImagePost


class ImageSerializer(serializers.ModelSerializer):
    '''
    After added context parameter in views image is the absolute path of file
    '''
    # photo_url = serializers.SerializerMethodField()

    username = serializers.SerializerMethodField('get_username_from_author')
    class Meta:
        model = ImagePost
        fields = ['image', 'slug', 'username']

    def get_username_from_author(self, image_post):
        username = image_post.author.username
        return username

    # def get_photo_url(self, ImagePost):
    #     request = self.context.get('request')
    #     photo_url = ImagePost.image.url
    #     return request.build_absolute_uri(photo_url)
