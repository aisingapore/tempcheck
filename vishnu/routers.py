from rest_framework import routers
from .views import EntryViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("entries", EntryViewSet, base_name="entry")
