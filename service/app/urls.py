from django.urls import path

from .views import VehicleModelsListView

urlpatterns = [
    path(
        "list",
        VehicleModelsListView.as_view(),
        name="vehicle-models-list",
    ),
]
