from django.db import models


class VehicleManufacture(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_manufacture_name")
        ]


class VehicleBody(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_body_name")
        ]


class VehicleModelYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["year"], name="unique_model_year")
        ]


class VehicleModel(models.Model):
    name = models.CharField(max_length=50)
    manufacture = models.ForeignKey(VehicleManufacture, on_delete=models.CASCADE)
    body = models.ManyToManyField(VehicleBody)
    year = models.ManyToManyField(VehicleModelYear)

    def __str__(self):
        return f"{self.manufacture.name} {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "manufacture"], name="unique_model")
        ]
