import pytest
from rest_framework import status

from ads.serialazers import AdListSerializer
from ads.tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ad_list = AdFactory.create_batch(10)
    response = client.get('/ad/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 10,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ad_list, many=True).data
    }

