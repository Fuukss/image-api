from rest_framework import serializers
from image.models import ImagePost


class ImageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = ImagePost
        fields = ['image', 'username']

    @staticmethod
    def get_username_from_author(image_post):
        username = image_post.author.username
        return username

    @staticmethod
    def validate_image_url(image_post):
        image = image_post.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return '%s%s' % ('http://localhost:8000', new_url)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ImagePostCreateSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['image', 'author']

    def save(self):
        try:
            image = self.validated_data['image']
            author = self.validated_data['author']
            image_post = ImagePost(
                author=author,
                image=image,
            )
            image_post.save()
            return image_post
        except KeyError:
            raise serializers.ValidationError({"response": "You must have an image."})

