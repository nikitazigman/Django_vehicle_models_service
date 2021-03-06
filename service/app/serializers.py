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


class VehicleVerificationSerializer(serializers.Serializer):
    model = serializers.CharField(write_only=True)
    year = serializers.IntegerField(write_only=True)
    body = serializers.CharField(write_only=True)
    manufacture = serializers.CharField(write_only=True)

    verification = serializers.SerializerMethodField()

    def get_verification(self, obj: dict) -> bool:
        if not VehicleModel.objects.filter(**obj).exists():
            return False

        return True

    def create(self):
        raise NotImplementedError(
            "Method is forbidden. Class can be used only for verification"
        )

    def save(self):
        raise NotImplementedError(
            "Method is forbidden. Class can be used only for verification"
        )
