from rest_framework.exceptions import ValidationError


def check_size_value(size):
    """
    Validator height and weight for thumbnail plan.
    """
    if size <= 0:
        raise ValidationError(
            {"response": "The value must be greater than zero."})
    else:
        return size
