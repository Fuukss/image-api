from rest_framework.exceptions import ValidationError
import os

IMAGE_SIZE_MAX_BYTES = 2000000
IMAGE_SIZE_EMPTY = 0


# Function to validate image size in model
def image_size(image):
    file_size = image.size

    if file_size > IMAGE_SIZE_MAX_BYTES:
        raise ValidationError(
            {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})
    elif file_size == IMAGE_SIZE_EMPTY:
        raise ValidationError(
            {"response": "That image probably isn't valid or is an empty file. Image must be less than 0 byte. "
                         "Try a different image."})
    else:
        return image


# Function to validate image format in model
def validate_file_extension(image):
    ext = os.path.splitext(image.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'File extension not supported. The supported extensions are: .jpg and .png. Try a different image.')
    return image
