from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serialazers import LocationSerializer


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
