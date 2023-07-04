import datetime

from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import SlugRelatedField
from ads.models import User, Location, Ad, Category, Selection


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
    age_of_born = SerializerMethodField()

    def get_age_of_born(self, obj):
        return datetime.date.today().year - obj.age

    class Meta:
        model = User
        fields = ['location', 'username', 'age_of_born']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

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

