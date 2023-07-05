import datetime

from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField, BooleanField
from rest_framework.relations import SlugRelatedField
from ads.models import User, Location, Ad, Category, Selection
from ads.validators import check_not_published


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserListSerializer(serializers.ModelSerializer):
    total_ads = IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'total_ads']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    locations = SlugRelatedField(slug_field='name', many=True, queryset=Location.objects.all(), required=False)

    def is_valid(self, *, raise_exception=False):
        for loc_name in self.initial_data.get('location', []):
            loc, _ = Location.objects.get_or_create(name=loc_name)
        return super().is_valid(raise_exception=raise_exception)

    class Meta:
        model = User
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserAdSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = User
        fields = ['location', 'username']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    user_locations = SerializerMethodField()

    def get_user_locations(self, obj):
        return [loc.name for loc in obj.author.location.all()]

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'category', 'user_locations']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    is_published = BooleanField(validators=[check_not_published], required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


