from app.logic.views import VerifyAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from .models import VehicleModel
from .serializers import VehicleModelSerializer


class VehicleModelsListView(generics.ListAPIView):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    filterset_fields = ["manufacture", "body", "year", "model"]

    @method_decorator(cache_page(60 * 60 * 24 * 30))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class VehicleModelVerificationView(VerifyAPIView):
    """the class checks existence of the vehicle model in service DB"""

    @method_decorator(cache_page(60 * 60 * 24 * 30))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
