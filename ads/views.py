import json

from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView

from HW_27 import settings
from ads.models import Category, Ad, User, Location


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = Category.objects.all()

        total_categories = self.object_list.count()
        page = int(request.GET.get("page", 0))
        offset = page * settings.TOTAL_ON_PAGE

        if offset > total_categories:
            self.object_list = []
        elif offset:
            self.object_list = self.object_list[offset:settings.TOTAL_ON_PAGE]
        else:
            self.object_list = self.object_list[:settings.TOTAL_ON_PAGE]

        result = []
        for cat in categories:
            result.append({
                    "id": cat.id,
                    "name": cat.name
                })

        response = {
            "items": result,
            "total": total_categories,
            "per_page": settings.TOTAL_ON_PAGE
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        new_cat = Category.objects.create(**cat_data)
        return JsonResponse({
            "id": new_cat.id,
            "name": new_cat.name
        })


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):

        try:
            cat = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "name" in data:
            self.object.name = data.pop("name")

        self.object.save()

        cat = self.get_object()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            "status": "ok"
        })


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        ads = Ad.objects.select_related("author").all()

        total_ads = self.object_list.count()
        page = int(request.GET.get("page", 0))
        offset = page * settings.TOTAL_ON_PAGE

        if offset > total_ads:
            self.object_list = []
        elif offset:
            self.object_list = self.object_list[offset:settings.TOTAL_ON_PAGE]
        else:
            self.object_list = self.object_list[:settings.TOTAL_ON_PAGE]

        result = []
        for ad in ads:
            result.append({
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author.username,
                    "price": ad.price
                })

        response = {
            "items": result,
            "total": total_ads,
            "per_page": settings.TOTAL_ON_PAGE
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, pk=ad_data.pop("author"))
        category = get_object_or_404(Category, name=ad_data.pop("category"))

        new_ad = Ad.objects.create(author=author, category=category, **ad_data)
        return JsonResponse({
            "id": new_ad.id,
            "name": new_ad.name,
            "author": new_ad.author.username,
            "price": new_ad.price,
            "description": new_ad.description,
            "category": new_ad.category.name,
            "image": new_ad.image.url if new_ad.image else None,
            "is_published": new_ad.is_published
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "image": ad.image.url if ad.image else None,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "name" in data:
            self.object.name = data.pop("name")
        if "price" in data:
            self.object.price = data.pop("price")
        if "description" in data:
            self.object.description = data.pop("description")
        if "category" in data:
            self.object.category.name = data.pop("category")

        self.object.save()

        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category,
            "image": ad.image,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            "status": "ok"
        })


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        users = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

        total_users = self.object_list.count()
        page = int(request.GET.get("page", 0))
        offset = page * settings.TOTAL_ON_PAGE

        if offset > total_users:
            self.object_list = []
        elif offset:
            self.object_list = self.object_list[offset:settings.TOTAL_ON_PAGE]
        else:
            self.object_list = self.object_list[:settings.TOTAL_ON_PAGE]

        result = []
        for user in users:
            result.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": user.location.name,
                "total_ads": user.total_ads
            })

        response = {
            "items": result,
            "total": total_users,
            "per_page": settings.TOTAL_ON_PAGE
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": user.location.name
            })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        location = Location.objects.get_or_create(name=user_data.pop("location"))

        new_user = User.objects.create(location=location, **user_data)

        return JsonResponse({
            "id": new_user.id,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "role": new_user.role,
            "age": new_user.age,
            "locations": new_user.location.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        data = json.loads(request.body)
        if "username" in data:
            self.object.username = data.pop("username")
        if "password" in data:
            self.object.password = data.pop("password")
        if "first_name" in data:
            self.object.first_name = data.pop("first_name")
        if "last_name" in data:
            self.object.last_name = data.pop("last_name")
        if "age" in data:
            self.object.age = data.pop("age")
        if "locations" in data:
            self.object.locations = data.pop("locations")

        self.object.save()

        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": user.location.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            "status": "ok"
        })

