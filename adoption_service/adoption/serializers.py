from rest_framework import serializers
from .models import AdoptionRequest


class AdoptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = [
            "id",
            "user_id",
            "animal_id",
            "appointment_id",
            "status",
            "date_requested",
        ]
        read_only_fields = [
            "id",
            "user_id", # Populated from Token
            "date_requested",
            "status",  # le statut est géré par le service (approve/reject)
        ]
