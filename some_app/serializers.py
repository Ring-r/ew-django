from rest_framework import serializers

from some_app.models import SomeEntity


class SomeEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SomeEntity
        fields = "__all__"
