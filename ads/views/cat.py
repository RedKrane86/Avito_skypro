import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView

from HW_27 import settings
from ads.models import Category


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
