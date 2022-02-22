from app.models import VehicleBody, VehicleManufacture, VehicleModel, VehicleModelYear
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase


class VehicleManufactureModelTest(TestCase):
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            VehicleManufacture.objects.create(name="test")
            VehicleManufacture.objects.create(name="test")


class VehicleBodyModelTest(TestCase):
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            VehicleBody.objects.create(name="test")
            VehicleBody.objects.create(name="test")


class VehicleModelYearTest(TestCase):
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            VehicleModelYear.objects.create(year=2020)
            VehicleModelYear.objects.create(year=2020)


class VehicleModelModelTest(TestCase):
    def test_unique_model(self):
        with self.assertRaises(IntegrityError):
            VehicleModel.objects.create(
                name="c40",
                manufacture=VehicleManufacture.objects.create(name="Volvo"),
            )
            VehicleModel.objects.create(
                name="c40",
                manufacture=VehicleManufacture.objects.create(name="Volvo"),
            )
