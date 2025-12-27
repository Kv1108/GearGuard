from django.db import models
from django.contrib.auth.models import User

class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(MaintenanceTeam, on_delete=models.CASCADE, related_name='technicians')

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('Production', 'Production'),
        ('IT', 'IT'),
        ('Facility', 'Facility'),
        ('Transport', 'Transport'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    department = models.CharField(max_length=100, help_text="e.g. Production, Admin, HR")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="The employee primarily using this equipment")
    
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    
    maintenance_team = models.ForeignKey(MaintenanceTeam, on_delete=models.SET_NULL, null=True, related_name='assigned_equipment')
    is_scrapped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class MaintenanceRequest(models.Model):
    TYPE_CHOICES = [
        ('Corrective', 'Corrective (Breakdown)'),
        ('Preventive', 'Preventive (Routine Checkup)'),
    ]
    
    STAGE_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Repaired', 'Repaired'),
        ('Scrap', 'Scrap'),
    ]

    subject = models.CharField(max_length=200)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Corrective')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='New')
    
    scheduled_date = models.DateField(null=True, blank=True, help_text="Required for Preventive Maintenance")
    duration = models.FloatField(default=0.0, help_text="Hours spent on repair")
    
    assigned_to = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.stage}] {self.subject} - {self.equipment.name}"
