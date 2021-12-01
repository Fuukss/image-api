def email_validator(email):
    if not email:
        raise ValueError("The given email must be set")


def username_validator(username):
    if not username:
        raise ValueError("The given username must be set")
