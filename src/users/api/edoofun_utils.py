from django.core.validators import validate_email
from django.core.exceptions import ValidationError




""" Validate Email """


def user_validate_email(email):
    try:
        email_valid = validate_email(email)
        return True
    except ValidationError:
        return False


""" genrate username """


def create_unique_username():
    try:
        username = generate_username(1)[0]
        while User.objects.filter(username=username).exists():
            username = generate_username(1)[0]
        return username
    except Exception as ex:
        logger.info(ex)
        logger.debug(ex)
        raise ValidationError("Username is not Created")


""" Genrate password """


def create_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", password)
    return password


