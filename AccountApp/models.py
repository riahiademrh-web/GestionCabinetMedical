from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


number_validator = RegexValidator(
    r'^\d{8}$', message="Le Numéro doit contenir exactement 8 chiffres."
)


def birth_date_validator(d):
    if d >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à la date du jour.")


class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
    )
    phone = models.CharField(max_length=8, validators=[number_validator])
    specialties = models.ManyToManyField("AccountApp.Specialty", related_name='Doctors')

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctors"

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}"


class Patient(User):
    national_id = models.CharField(
        max_length=8, unique=True, validators=[number_validator]
    )
    phone = models.CharField(max_length=8, validators=[number_validator])
    birth_date = models.DateField(validators=[birth_date_validator])

    class Meta:
        verbose_name = "patient"
        verbose_name_plural = "patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Specialty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "specialties"

    def __str__(self):
        return self.name