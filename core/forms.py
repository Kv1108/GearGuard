from django import forms
from .models import Equipment, MaintenanceRequest, MaintenanceTeam, Technician, WorkCenter, EquipmentCategory, MaintenanceLog

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
            'assigned_date': forms.DateInput(attrs={'type': 'date'}),
            'scrap_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'subject', 'request_type', 'priority', 'stage', 
            'equipment', 'work_center',
            'scheduled_date', 'assigned_to', 'duration', 'instructions'
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}), # Using date for simplicity, can handle datetime if needed
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'assigned_to': 'Assigned Technician'
        }

    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get('equipment')
        work_center = cleaned_data.get('work_center')
        request_type = cleaned_data.get('request_type')
        scheduled_date = cleaned_data.get('scheduled_date')

        if not equipment and not work_center:
            raise forms.ValidationError("You must select either an Equipment or a Work Center.")
        
        if request_type == 'Preventive' and not scheduled_date:
            self.add_error('scheduled_date', 'Scheduled date is required for preventive maintenance.')
        
        return cleaned_data

class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a note or update...'})
        }

class WorkCenterForm(forms.ModelForm):
    class Meta:
        model = WorkCenter
        fields = '__all__'
