from app.models import VehicleModel
from django.db.utils import IntegrityError
from django.test import TestCase


class VehicleModelModelTest(TestCase):
    def test_unique_model(self):
        with self.assertRaises(IntegrityError):
            VehicleModel.objects.create(
                model="c40", manufacture="Volvo", year=2005, body="Sedan"
            )
            VehicleModel.objects.create(
                model="c40", manufacture="Volvo", year=2005, body="Sedan"
            )

    def test_body_choices(self):
        with self.assertRaises(IntegrityError):
            VehicleModel.objects.create(
                model="c40", manufacture="Volvo", year=2005, body="sdan"
            )
