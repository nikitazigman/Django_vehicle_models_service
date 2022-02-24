from app.models import VehicleModel
from app.serializers import VehicleModelSerializer, VehicleVerificationSerializer
from django.core.management import call_command
from django.test import TestCase
from rest_framework.serializers import ValidationError


class VehicleModelModelTest(TestCase):
    # Be careful, validation does not work with option many=True
    def test_unique_validation(self):
        model = {"year": 1992, "manufacture": "Volvo", "model": "960", "body": "Sedan"}
        with self.assertRaises(ValidationError):
            for _ in range(2):
                serializer = VehicleModelSerializer(data=model)
                serializer.is_valid(raise_exception=True)
                serializer.save()


class VehicleModelVerificationSerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("addvehiclemodels", limit=1)

    def setUp(self):
        serializer = VehicleModelSerializer(VehicleModel.objects.first())
        self.data = serializer.data
        self.data.pop("id")

    def test_varify_valid_data(self):
        serializer = VehicleVerificationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.data["verification"])

    def test_varify_invalid_data(self):
        self.data["model"] = "wrong model"

        serializer = VehicleVerificationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.data["verification"])

    def test_data_error(self):
        self.data["model"] = [1, 2, 3]

        serializer = VehicleVerificationSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
