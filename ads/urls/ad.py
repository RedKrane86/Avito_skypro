from django.urls import path
from rest_framework import routers

from ads.views.ad import AdCreateView, AdUpdateView, AdDeleteView, AdViewSet

urlpatterns = [

    path('create/', AdCreateView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
]

router = routers.SimpleRouter
router.register("", AdViewSet)
urlpatterns += router.urls
