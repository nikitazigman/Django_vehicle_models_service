from django.urls import path

from .views import (
    VehicleBodyListView,
    VehicleManufactureListView,
    VehicleModelsListView,
)

urlpatterns = [
    path(
        "vehicle-models-list",
        VehicleModelsListView.as_view(),
        name="vehicle-models-list",
    ),
    path(
        "vehicle-bodies-list", VehicleBodyListView.as_view(), name="vehicle-bodies-list"
    ),
    path(
        "vehicle-manufactures-list",
        VehicleManufactureListView.as_view(),
        name="vehicle-manufactures-list",
    ),
]
