from rest_framework.exceptions import ValidationError


def check_time_value(time):
    """
    Validator time value.
    """
    if time < 300:
        raise ValidationError(
            {"response": "The value must be greater than 300."})
    if time > 50000:
        raise ValidationError(
            {"response": "The value must be lg than 50000."})
    return time

