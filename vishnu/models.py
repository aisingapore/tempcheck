from django.contrib.auth.models import User

# pylint: disable=no-member
# Ensure only unique emails in DB
User._meta.get_field('email')._unique = True 
