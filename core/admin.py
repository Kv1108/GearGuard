from django.contrib import admin
from .models import MaintenanceTeam, Technician, Equipment, MaintenanceRequest

@admin.register(MaintenanceTeam)
class MaintenanceTeamAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'department', 'maintenance_team', 'is_scrapped')
    list_filter = ('category', 'department', 'maintenance_team', 'is_scrapped')
    search_fields = ('name', 'serial_number')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'equipment', 'request_type', 'stage', 'assigned_to', 'scheduled_date')
    list_filter = ('request_type', 'stage', 'scheduled_date')
    search_fields = ('subject', 'equipment__name')
