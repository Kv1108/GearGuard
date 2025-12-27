from django.contrib import admin
from .models import MaintenanceTeam, Technician, Equipment, MaintenanceRequest, WorkCenter, EquipmentCategory, MaintenanceLog

@admin.register(MaintenanceTeam)
class MaintenanceTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('members',)

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsible_user')

@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'efficiency', 'oee_target')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'work_center', 'department', 'is_scrapped', 'health')
    list_filter = ('category', 'department', 'maintenance_team', 'is_scrapped', 'work_center')
    search_fields = ('name', 'serial_number')

class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 0

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'get_target', 'request_type', 'stage', 'priority', 'assigned_to', 'scheduled_date')
    list_filter = ('request_type', 'stage', 'priority', 'scheduled_date')
    search_fields = ('subject', 'equipment__name', 'work_center__name')
    inlines = [MaintenanceLogInline]

    def get_target(self, obj):
        return obj.equipment if obj.equipment else obj.work_center
    get_target.short_description = 'Target'
