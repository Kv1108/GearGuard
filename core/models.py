from django.db import models
from django.contrib.auth.models import User

# --- Core Setup Models ---

class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # V2: Team members
    members = models.ManyToManyField(User, related_name='maintenance_teams', blank=True)

    def __str__(self):
        return self.name

class Technician(models.Model):
    # Kept for backward compatibility or specifically for primary role, 
    # but Team members M2M is more flexible.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(MaintenanceTeam, on_delete=models.CASCADE, related_name='technicians')

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    responsible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_categories')

    class Meta:
        verbose_name_plural = "Equipment Categories"

    def __str__(self):
        return self.name

class WorkCenter(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    efficiency = models.FloatField(default=100.0, help_text="Efficiency percentage")
    oee_target = models.FloatField(default=85.0, help_text="OEE Target percentage")
    
    def __str__(self):
        return f"{self.name} ({self.code})"

# --- Asset Models ---

class Equipment(models.Model):
    # V2: Updated fields
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    
    # Replaced char field with FK
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, related_name='equipment')
    work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipment')
    
    department = models.CharField(max_length=100, help_text="Usage Department")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_equipment')
    
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    assigned_date = models.DateField(null=True, blank=True)
    scrap_date = models.DateField(null=True, blank=True)
    
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    maintenance_team = models.ForeignKey(MaintenanceTeam, on_delete=models.SET_NULL, null=True, related_name='assigned_equipment')
    is_scrapped = models.BooleanField(default=False)
    health = models.IntegerField(default=100, help_text="Equipment health percentage (0-100)")

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

# --- Maintenance Workflow Models ---

class MaintenanceRequest(models.Model):
    TYPE_CHOICES = [
        ('Corrective', 'Corrective (Breakdown)'),
        ('Preventive', 'Preventive (Routine Checkup)'),
    ]
    
    # V2: Updated stages
    STAGE_CHOICES = [
        ('New', 'New Request'),
        ('In Progress', 'In Progress'),
        ('Repaired', 'Repaired'),
        ('Scrap', 'Scrap'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    subject = models.CharField(max_length=200)
    
    # Can be linked to Equipment OR Work Center
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True, related_name='requests')
    work_center = models.ForeignKey(WorkCenter, on_delete=models.CASCADE, null=True, blank=True, related_name='requests')
    
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Corrective') # maintenance_type
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='New') # status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    
    scheduled_date = models.DateTimeField(null=True, blank=True) # scheduled_at
    duration = models.FloatField(default=0.0, help_text="Hours spent")
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests') # Technician/User
    team = models.ForeignKey(MaintenanceTeam, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.equipment and not self.work_center:
            raise ValidationError("Either Equipment or Work Center must be selected.")

    def __str__(self):
        target = self.equipment.name if self.equipment else (self.work_center.name if self.work_center else "Unknown")
        return f"[{self.stage}] {self.subject} - {target}"

class MaintenanceLog(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='logs')
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log by {self.created_by} on {self.request}"
