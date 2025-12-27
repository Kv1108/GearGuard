from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaintenanceRequest

@receiver(post_save, sender=MaintenanceRequest)
def check_scrap_condition(sender, instance, created, **kwargs):
    """
    If a request is moved to 'Scrap', mark the equipment as scrapped.
    """
    if instance.stage == 'Scrap':
        equipment = instance.equipment
        if not equipment.is_scrapped:
            equipment.is_scrapped = True
            equipment.save()
