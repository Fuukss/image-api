from rest_framework import serializers

from image.models import ImagePost


class ImageSerializer(serializers.ModelSerializer):
    '''
    After added context parameter in views image is the absolute path of file
    '''
    # photo_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagePost
        fields = ['author', 'image', 'slug']

    # def get_photo_url(self, ImagePost):
    #     request = self.context.get('request')
    #     photo_url = ImagePost.image.url
    #     return request.build_absolute_uri(photo_url)
