from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from some_app.models import SomeEntity
from some_app.serializers import SomeEntitySerializer


class SomeEntityViewSet(viewsets.ModelViewSet):
    queryset = SomeEntity.objects.all()
    serializer_class = SomeEntitySerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="some_parameter",
                description="some description",
                required=True,
                type=str,
            ),
        ],
        responses={200: SomeEntitySerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="some-action")
    def some_action(self, request):
        some_parameter = request.query_params.get("some_parameter")

        if not some_parameter:
            return Response({"error": "some_parameter id required."}, status=400)

        try:
            some_intity_s = self.queryset.filter(
                # ...
            )
            serializer = self.get_serializer(some_intity_s, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "some eror."}, status=400)
