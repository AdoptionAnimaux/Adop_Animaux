from django.db import models


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    # ID de l'utilisateur venant du JWT (account_service)
    user_id = models.IntegerField()

    # ID de l'animal venant de animals_service
    animal_id = models.IntegerField()

    appointment_id = models.IntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AdoptionRequest #{self.id} | user={self.user_id} animal={self.animal_id}"
