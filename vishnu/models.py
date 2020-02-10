from django.db import models

class Entry(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    # coordinate dec places referencing google's limits
    # source: https://stackoverflow.com/questions/30706799/
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    long = models.DecimalField(max_digits=22, decimal_places=16)
    # file upload: local for now
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    owner = models.ForeignKey("auth.User", related_name="records", on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
