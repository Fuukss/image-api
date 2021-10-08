from rest_framework import serializers
from image.models import ImagePost


class ImageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = ImagePost
        fields = ['image', 'username']

    def get_username_from_author(self, image_post):
        username = image_post.author.username
        return username

    def validate_image_url(self, image_post):
        image = image_post.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return '%s%s' % ('http://localhost:8000', new_url)


class ImagePostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['image', 'slug', 'author']

    def save(self):
        try:
            image = self.validated_data['image']
            slug = self.validated_data['slug']
            image_post = ImagePost(
                author=self.validated_data['author'],
                slug=slug,
                image=image,
            )
            image_post.save()
            return image_post

        except KeyError:
            raise serializers.ValidationError({"response": "You must have a slug (can be empty) and an image."})
