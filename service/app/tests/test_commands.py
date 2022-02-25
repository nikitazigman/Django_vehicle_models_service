import json
from pathlib import Path

from app.models import VehicleModel
from app.serializers import VehicleModelSerializer
from django.core.management import call_command
from django.test import TestCase


class AddVehicleModelsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        vehicle_model_path = (
            Path(__file__)
            .resolve()
            .parent.parent.parent.joinpath(
                "staticfiles/vehicle_models/vehicle-model-dataset.json"
            )
        )
        with open(vehicle_model_path, "r") as f:
            cls.data = json.load(f)

    def test_correct_storing_db(self):
        models_number = 2
        call_command("addvehiclemodels", limit=models_number)

        vehicle_models = VehicleModel.objects.all()

        self.assertEqual(vehicle_models.count(), models_number)

        for row_data, vehicle_model in zip(
            self.data[:models_number], vehicle_models
        ):
            serializer = VehicleModelSerializer(vehicle_model)
            model_data = serializer.data
            model_data.pop("id")
            self.assertEquals(row_data, model_data)
