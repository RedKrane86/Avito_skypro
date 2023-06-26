from rest_framework import routers

from ads.views.loc import LocationViewSet

router = routers.SimpleRouter
router.register("", LocationViewSet)
urlpatterns = router.urls
