from django.urls import path

from .views import VehicleModelsListView, VehicleModelVerificationView

urlpatterns = [
    path(
        "list",
        VehicleModelsListView.as_view(),
        name="vehicle-models-list",
    ),
    path(
        "verify/",
        VehicleModelVerificationView.as_view(),
        name="model-verification",
    ),
]
