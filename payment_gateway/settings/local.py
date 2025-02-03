from .base import * # noqa: F403
from decouple import config

DEBUG=config('DEBUG')

ALLOWED_HOSTS=config('ALLOWED_HOSTS').split(',')

print("Running from local env")