from django.urls import path
from rest_framework import routers

from ads.views.ad import AdUpdateView, AdDeleteView, AdViewSet

urlpatterns = [

    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
]

router = routers.SimpleRouter()
router.register("", AdViewSet)
urlpatterns += router.urls
