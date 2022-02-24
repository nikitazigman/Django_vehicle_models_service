from app.serializers import VehicleVerificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class VerifyAPIView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = VehicleVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, 200)
