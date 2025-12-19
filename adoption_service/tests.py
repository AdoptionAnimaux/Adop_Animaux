from django.test import TestCase

# Create your tests here.
from adoption.messaging.producer import publish_adoption

publish_adoption({
    "event": "adoption_approved",
    "user_id": 1,
    "animal_id": 99,
    "animal_name": "Test Animal"
})
