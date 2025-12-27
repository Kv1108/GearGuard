from django import forms
from .models import Equipment, MaintenanceRequest, MaintenanceTeam, Technician

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'subject', 'equipment', 'request_type', 'scheduled_date', 
            'assigned_to', 'stage', 'duration'
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'stage': forms.Select(attrs={'class': 'status-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        scheduled_date = cleaned_data.get('scheduled_date')

        if request_type == 'Preventive' and not scheduled_date:
            self.add_error('scheduled_date', 'Scheduled date is required for preventive maintenance.')
        
        return cleaned_data
