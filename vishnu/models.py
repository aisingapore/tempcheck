from django.contrib.auth.models import User

# Ensure only unique emails in DB
# pylint: disable=no-member
User._meta.get_field('email')._unique = True
