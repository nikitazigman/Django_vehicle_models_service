from django.db import models


class Bodies(models.TextChoices):
    Sedan = "Sedan", "Sedan"
    Hatchback = "Hatchback", "Hatchback"
    SUV2020 = "SUV2020", "SUV2020"
    SUV1992 = "SUV1992", "SUV1992"
    SUV = "SUV", "SUV"
    Pickup = "Pickup", "Pickup"
    Coupe = "Coupe", "Coupe"
    Van_Minivan = "Van/Minivan", "Van/Minivan"
    Wagon = "Wagon", "Wagon"
    Convertible = "Convertible", "Convertible"


class VehicleModel(models.Model):
    model = models.CharField(max_length=50)
    manufacture = models.CharField(max_length=100)
    body = models.CharField(max_length=100, choices=Bodies.choices)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.manufacture} {self.model} {self.body} {self.year}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["model", "manufacture", "body", "year"], name="unique_model"
            ),
            models.CheckConstraint(
                name="check_body_choices",
                check=models.Q(body__in=Bodies.values),
            ),
        ]
