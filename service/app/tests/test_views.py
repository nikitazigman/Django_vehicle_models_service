from app.models import VehicleBody, VehicleManufacture, VehicleModel, VehicleModelYear
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("addvehiclemodels", 2)
        user = User.objects.create_user(username="username", password="password")

    def setUp(self):
        self.assertTrue(self.client.login(username="username", password="password"))

    def test_can_get_models(self):
        response = self.client.get(reverse("vehicle-models-list"))

        self.assertEqual(response.status_code, 200)

        models = VehicleModel.objects.all()
        self.assertEqual(len(response.json()), len(models))

        for check_model, resp_model in zip(models, response.json()):
            self.assertEqual(check_model.name, resp_model["name"])

    def test_can_filter_models_by_body(self):
        body_filter = VehicleBody.objects.first()

        response = self.client.get(
            reverse("vehicle-models-list"), {"body": body_filter.id}
        )

        self.assertEqual(response.status_code, 200)

        expected_models = VehicleModel.objects.filter(body=body_filter)
        self.assertEqual(len(response.json()), len(expected_models))

        for check_model, resp_model in zip(expected_models, response.json()):
            self.assertEqual(check_model.name, resp_model["name"])

    def test_can_filter_models_by_year(self):
        year_filter = VehicleModelYear.objects.first()

        response = self.client.get(
            reverse("vehicle-models-list"), {"year": year_filter.id}
        )

        self.assertEqual(response.status_code, 200)

        expected_models = VehicleModel.objects.filter(year=year_filter)
        self.assertEqual(len(response.json()), len(expected_models))

        for check_model, resp_model in zip(expected_models, response.json()):
            self.assertEqual(check_model.name, resp_model["name"])

    def test_can_filter_models_by_manufacture(self):
        manufacture_filter = VehicleManufacture.objects.first()

        response = self.client.get(
            reverse("vehicle-models-list"), {"manufacture": manufacture_filter.id}
        )

        self.assertEqual(response.status_code, 200)

        expected_models = VehicleModel.objects.filter(manufacture=manufacture_filter)
        self.assertEqual(len(response.json()), len(expected_models))

        for check_model, resp_model in zip(expected_models, response.json()):
            self.assertEqual(check_model.name, resp_model["name"])

    def test_can_get_bodies(self):
        response = self.client.get(reverse("vehicle-bodies-list"))

        self.assertEqual(response.status_code, 200)

        bodies = VehicleBody.objects.all()
        self.assertEqual(len(response.json()), len(bodies))

        for check_body, resp_model in zip(bodies, response.json()):
            self.assertEqual(check_body.name, resp_model["name"])

    def test_can_get_manufactures(self):
        response = self.client.get(reverse("vehicle-manufactures-list"))

        self.assertEqual(response.status_code, 200)
        manufactures = VehicleManufacture.objects.all()

        self.assertEqual(len(response.json()), len(manufactures))

        for check_manufacture, resp_model in zip(manufactures, response.json()):
            self.assertEqual(check_manufacture.name, resp_model["name"])
