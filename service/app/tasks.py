from typing import Dict, Tuple

from celery import shared_task

from .serializers import VehicleVerificationSerializer


@shared_task(
    name="vehicle_model_service.verify_model",
    bind=True,
    rate_limit="100/s",
    acks_late=True,
)
def model_verification(
    self, model: str, year: int, manufacture: str, body: str
) -> Tuple[bool, Dict]:
    # ToDo add cache here
    serializer = VehicleVerificationSerializer(
        data={
            "model": model,
            "year": year,
            "body": body,
            "manufacture": manufacture,
        }
    )

    if serializer.is_valid():
        return True, serializer.data
    else:
        return False, serializer.errors
