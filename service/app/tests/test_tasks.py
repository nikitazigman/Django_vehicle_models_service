from app.models import VehicleModel
from app.tasks import model_verification
from django.core.management import call_command
from django.test import TestCase


class TasksTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("addvehiclemodels", limit=2)

    def test_tasks_supported_model(self):
        model = VehicleModel.objects.first()
        status, result = model_verification(
            model.model,
            model.year,
            model.manufacture,
            model.body,
        )
        self.assertTrue(status)
        self.assertTrue(result["verification"])

    def test_tasks_unsupported_model(self):
        model = VehicleModel.objects.first()
        status, result = model_verification(
            model.model + "mock",
            model.year,
            model.manufacture,
            model.body,
        )
        self.assertTrue(status)
        self.assertFalse(result["verification"])

    def test_tasks_wrong_typing(self):
        model = VehicleModel.objects.first()
        status, result = model_verification(
            [1, 2, 3],
            model.year,
            model.manufacture,
            model.body,
        )
        self.assertFalse(status)
        self.assertTrue("model" in result)
