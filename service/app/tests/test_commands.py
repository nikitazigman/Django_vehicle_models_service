import json

import requests
from app.models import VehicleBody, VehicleManufacture, VehicleModel, VehicleModelYear
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase


class AddVehicleModelsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.limit = 1
        cls.url = f"https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?order=Year&limit={cls.limit}"
        cls.headers = {
            "X-Parse-Application-Id": "v0mZ5eDsC6ltQlp634YY6g8QrhYLSGteFNIBN8Uy",
            "X-Parse-REST-API-Key": "9TRyYtzfPcJHtygxiL1mv6xkGGVBriHfByq3eBup",
        }
        cls.years = set()
        cls.manufactures = set()
        cls.bodies = set()
        cls.models = set()

        cls.data = json.loads(
            requests.get(cls.url, headers=cls.headers).content.decode("utf-8")
        )

    def test_correct_storing_db(self):
        call_command("addvehiclemodels", self.limit)

        for result in self.data["results"]:
            self.models.add(result["Model"])
            self.years.add(result["Year"])
            self.manufactures.add(result["Make"].strip())
            self.bodies.update([s.strip() for s in result["Category"].split(",")])

        years = list(VehicleModelYear.objects.values_list("year", flat=True))
        bodies = list(VehicleBody.objects.values_list("name", flat=True))
        manufactures = list(VehicleManufacture.objects.values_list("name", flat=True))
        models = list(VehicleModel.objects.values_list("name", flat=True))

        expected_years = list(self.years)
        expected_bodies = list(self.bodies)
        expected_manufactures = list(self.manufactures)
        expected_models = list(self.models)

        self.assertEqual(years.sort(), expected_years.sort())
        self.assertEqual(bodies.sort(), expected_bodies.sort())
        self.assertEqual(manufactures.sort(), expected_manufactures.sort())
        self.assertEqual(models.sort(), expected_models.sort())
