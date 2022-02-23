from app.models import Bodies, VehicleModel
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("addvehiclemodels", limit=2)
        User.objects.create_user(username="username", password="password")

    def setUp(self):
        self.assertTrue(self.client.login(username="username", password="password"))

    def test_can_get_models(self):
        response = self.client.get(reverse("vehicle-models-list"))

        self.assertEqual(response.status_code, 200)
        requested_models = response.json()

        models_number = VehicleModel.objects.all().count()
        self.assertEqual(len(requested_models), models_number)

        requested_model = requested_models[0]

        self.assertTrue(requested_model.get("model"))
        self.assertTrue(requested_model.get("manufacture"))
        self.assertTrue(requested_model.get("body"))
        self.assertTrue(requested_model.get("year"))

    def test_can_filter_models_by_body(self):
        response = self.client.get(
            reverse("vehicle-models-list"), {"body": Bodies.Hatchback.value}
        )

        self.assertEqual(response.status_code, 200)
        requested_models = response.json()

        models_number = VehicleModel.objects.filter(body=Bodies.Hatchback.value).count()
        self.assertEqual(len(requested_models), models_number)

    def test_can_filter_models_by_year(self):
        year_filter = VehicleModel.objects.first().year
        response = self.client.get(
            reverse("vehicle-models-list"), {"year": year_filter}
        )

        self.assertEqual(response.status_code, 200)
        requested_models = response.json()

        models_number = VehicleModel.objects.filter(year=year_filter).count()
        self.assertEqual(len(requested_models), models_number)

    def test_can_filter_models_by_manufacture(self):
        manufacture_filter = VehicleModel.objects.first().manufacture
        response = self.client.get(
            reverse("vehicle-models-list"), {"manufacture": manufacture_filter}
        )

        self.assertEqual(response.status_code, 200)
        requested_models = response.json()

        models_number = VehicleModel.objects.filter(
            manufacture=manufacture_filter
        ).count()
        self.assertEqual(len(requested_models), models_number)
