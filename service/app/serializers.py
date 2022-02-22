from rest_framework import serializers, validators

from .models import VehicleBody, VehicleManufacture, VehicleModel, VehicleModelYear


class VehicleBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBody
        fields = ["name", "id"]


class VehicleManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleManufacture
        fields = ["name", "id"]


class VehicleModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModelYear
        fields = ["year", "id"]


class VehicleModelSerializer(serializers.ModelSerializer):
    body = VehicleBodySerializer(read_only=True, many=True)
    manufacture: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True, many=False, slug_field="name"
    )
    year: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field="year"
    )

    class Meta:
        model = VehicleModel
        fields = ["id", "name", "year", "body", "manufacture"]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=VehicleModel.objects.all(), fields=["name", "manufacture"]
            )
        ]
