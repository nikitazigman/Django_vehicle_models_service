from rest_framework import generics

from .models import VehicleModel
from .serializers import VehicleModelSerializer


class VehicleModelsListView(generics.ListAPIView):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    filterset_fields = ["manufacture", "body", "year", "model"]


# class VehicleBodyListView(generics.ListAPIView):
#     queryset = VehicleBody.objects.all()
#     serializer_class = VehicleBodySerializer
#
#
# class VehicleManufactureListView(generics.ListAPIView):
#     queryset = VehicleManufacture.objects.all()
#     serializer_class = VehicleManufactureSerializer
