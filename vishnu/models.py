from django.db import models
from django.contrib.auth.models import User

def append_owner_email(instance, filename):
    """
    function for upload to to create a subdirectory for each user
    based on his name, so upload_to="uploads/{owner_name}"
    """
    filename = "uploads/{}/{}".format(instance.owner.email, filename)
    return filename
class Entry(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    # coordinate dec places referencing google's limits
    # source: https://stackoverflow.com/questions/30706799/
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    long = models.DecimalField(max_digits=22, decimal_places=16)
    file = models.ImageField(upload_to=append_owner_email)
    owner = models.ForeignKey("auth.User", related_name="records", on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

# Ensure only unique emails in DB
# pylint: disable=no-member
User._meta.get_field('email')._unique = True
