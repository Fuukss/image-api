from rest_framework.exceptions import ValidationError
import os

IMAGE_SIZE_MAX_BYTES = 2_000_000
IMAGE_SIZE_EMPTY = 0


def image_size(image):
    try:
        if image.size <= IMAGE_SIZE_MAX_BYTES:
            return image
        else:
            raise ValidationError(
                {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
    except:
        if image.size == IMAGE_SIZE_EMPTY:
            raise ValidationError(
                {
                    "response": "That image probobly is valid or is a empty file. Images must be less than 0 byte. "
                                "Try a different image."})


def validate_file_extension(image):
    ext = os.path.splitext(image.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.JPG', '.PNG']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'File extension not supported. The supported extensions are: .jpg and .png. Try a different image.')
