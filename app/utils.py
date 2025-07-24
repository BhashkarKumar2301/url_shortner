import string
import random
import validators

def generate_short_code(length=6):
    """
    Generate a random alphanumeric short code of given length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    """
    Validate the given URL using the validators package.
    Returns True if valid, False otherwise.
    """
    return validators.url(url)
