from rest_framework import serializers, validators

from .models import VehicleModel


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ["id", "model", "year", "body", "manufacture"]

        # Be careful, validation does not work with option many=True
        validators = [
            validators.UniqueTogetherValidator(
                queryset=VehicleModel.objects.all(),
                fields=["model", "manufacture", "year", "body"],
            )
        ]
