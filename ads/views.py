import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView

from HW_27 import settings
from ads.models import Category, Ad, User


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        total_categories = self.orbject_list.count()
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

        self.object.name = data.pop("name")
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
        ads = Ad.objects.all()
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

        self.object.name = data.pop("name")
        self.object.price = data.pop("price")
        self.object.description = data.pop("description")
        self.object.category.name = data.pop("category")

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
