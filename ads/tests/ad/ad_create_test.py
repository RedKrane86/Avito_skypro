import pytest
from rest_framework import status


@pytest.mark.django_db
def test_ad_create(client, user, category, access_token):
    data = {
        'author': user.username,
        'category': category.name,
        'name': 'test_for_test',
        'price': 100
    }

    expected_data = {
        'id': 1,
        'category': category.name,
        'author': user.username,
        'is_published': False,
        'name': 'test_for_test',
        'price': 100,
        'description': None,
        'image': None
    }

    response = client.post('/ad/', data=data, HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
