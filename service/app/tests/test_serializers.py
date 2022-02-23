from copy import deepcopy

from app.serializers import VehicleModelSerializer
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
