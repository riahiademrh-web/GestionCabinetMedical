from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Status(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmé'
    CANCELLED = 'CANCELLED', 'Annulé'


class Appointment(models.Model):
    doctor = models.ForeignKey(
        'AccountApp.Doctor', on_delete=models.CASCADE, related_name='appointments'
    )
    patient = models.ForeignKey(
        'AccountApp.Patient', on_delete=models.CASCADE, related_name='appointments'
    )
    reason = models.TextField()
    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date',
            )
        ]

    def clean(self):
        super().clean()
        if not self.appointment_date:
            return
        date_changed = True
        if not self._state.adding:
            old_date = (
                Appointment.objects.filter(pk=self.pk)
                .values_list('appointment_date', flat=True)
                .first()
            )
            date_changed = old_date != self.appointment_date
        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError(
                {'appointment_date': "La date doit être postérieure à la date et l'heure actuelles."}
            )

    def __str__(self):
        return f"RDV {self.appointment_date:%d/%m/%Y %H:%M} : {self.patient} avec {self.doctor}"